import asyncio
import base64
from datetime import datetime, timezone
import re
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from os import getenv
from settingsmanager import read_config, write_config
from utils.database import test_db_connection, init_db, close_db_connection, get_collection
from utils.create_user_json import create_user_json
from utils.restart import restart_app
from utils.unencrypt_and_hash import unecrypt_and_hash
from uuid import uuid4

load_dotenv()

# Configs from settingsmanager
try:
    setup_complete = read_config().get("global").get("setup_complete") # pyright: ignore[reportOptionalMemberAccess]
except AttributeError:
    setup_complete = False

api = APIRouter(tags=["api"])


@api.get("/health")
def healthcheck():
    return {
        "status": "healthy",
        "edition": "lite",
        "version": getenv("VERSION", "1.0.0"),  # set during build process in the CI/CD Pipeline(gh actions)
    }


@api.post("/setup-info")
async def setup_info(
        request: Request,
        response: Response,
):
    if setup_complete:
        return JSONResponse(
            {"error": "SetupAlreadyCompleted", "error_description": "The setup has already been completed."},
            status_code=400,
        )
    # Validate content type
    content_type = request.headers.get("content-type", "")
    if "application/json" not in content_type:
        return JSONResponse(
            {"error": "InvalidContentType", "error_description": "Content-Type must be application/json."},
            status_code=415,
        )
    # Parse JSON safely
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            {"error": "InvalidJSON", "error_description": "Request body must be valid JSON."},
            status_code=400,
        )

    decoded_bytes = base64.b64decode(payload.get("mongo_url"))
    # Convert bytes to a string (assuming UTF-8 encoding)
    favicon_url = payload.get("favicon_url", "/static/img/favicon.ico")
    theme_color = payload.get("theme_color", "#0925C2")
    instance_name = payload.get("instance_name", "wOpenChat-Lite")
    mongo_url_b64 = payload.get("mongo_url")

    if not mongo_url_b64 or not isinstance(mongo_url_b64, str):
        return JSONResponse({"error": "MissingField", "error_description": "Field 'mongo_url' is required."},
                            status_code=422)

    try:
        decoded_bytes = base64.b64decode(mongo_url_b64, validate=True)
        mongo_url = decoded_bytes.decode("utf-8")
    except Exception:
        return JSONResponse({"error": "InvalidMongoURL", "error_description": "mongo_url must be valid base64."},
                            status_code=422)

    if not mongo_url or not isinstance(mongo_url, str) or not mongo_url.strip():
        return JSONResponse(
            {"error": "MissingField", "error_description": "Field 'mongo_url' is required."},
            status_code=422,
        )

    if not re.match(r'^mongodb(\+srv)?://.*', mongo_url):
        return JSONResponse(
            {"error": "InvalidMongoURL", "error_description": "The provided MongoDB URL is not valid."},
            status_code=422,
        )

    if await test_db_connection(mongo_url) is False:
        return JSONResponse(
            {"error": "DatabaseConnectionFailed",
             "error_description": "Failed to connect to the database with the provided MongoDB URL. Check the logs for more information. Setup aborted."},
            status_code=400,
        )

    await init_db() # Temporarily initialize DB for admin user creation

    write_config({
        "global": {
            "setup_complete": True,
            "instance_name": instance_name,
        },
        "customization": {
            "favicon_url": favicon_url,
            "theme_color": theme_color
        },
        "mongo_url": mongo_url.strip(),
        "secret_key": str(uuid4())
    })

    # Then now admin users will be created
    admin_username = payload.get("admin_username")
    if not admin_username or not isinstance(admin_username, str) or not admin_username.strip():
        return JSONResponse(
            {"error": "MissingField", "error_description": "Field 'admin_username' is required."},
            status_code=422,
        )
    admin_email = payload.get("admin_email")
    if not admin_email or not isinstance(admin_email, str) or not admin_email.strip():
        return JSONResponse(
            {"error": "MissingField", "error_description": "Field 'admin_email' is required."},
            status_code=422,
        )
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', admin_email):
        return JSONResponse(
            {"error": "InvalidEmail", "error_description": "The provided admin email is not valid."},
            status_code=422,
        )
    admin_password = unecrypt_and_hash(data=payload.get("admin_password"))
    
    if not admin_password or not isinstance(admin_password, str) or not admin_password.strip():
        return JSONResponse(
            {"error": "MissingField", "error_description": "Field 'admin_password' is required."},
            status_code=422,
        )
    if len(admin_password) < 8:
        return JSONResponse(
            {"error": "WeakPassword", "error_description": "Admin password must be at least 8 characters long."},
            status_code=400,
        )

    # now to actually create the admin user
    users = await get_collection("users")

    # Insert the admin user into the database
    await users.insert_one(
        create_user_json(
            username=admin_username.strip(),
            email=admin_email.strip(),
            password=admin_password.strip(),
            admin=True,
            enabled=True,
            created_at=str(datetime.now(timezone.utc)),
        )
    )

    # Close the temporary DB connection
    close_db_connection()

    task = asyncio.create_task(restart_app()) # Restart the app to apply changes

    return JSONResponse({
        "success": True,
        "message": "Setup complete, restarting wOpenChat-Lite to apply changes."
    })