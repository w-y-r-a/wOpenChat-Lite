import re

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from os import getenv
from settingsmanager import read_config, write_config
from utils.database import test_db_connection

load_dotenv()

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
    if read_config("Global", "setup_complete", cast=lambda v: v.lower() == "true"):
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

    instance_name = payload.get("instance_name", "wOpenChat-Lite")
    mongo_url = payload.get("mongo_url")

    if not mongo_url or not isinstance(mongo_url, str) or not mongo_url.strip():
        return JSONResponse(
            {"error": "MissingField", "error_description": "Field 'mongo_url' is required."},
            status_code=400,
        )

    if not re.match(r'^mongodb(\+srv)?://.*', mongo_url):
        return JSONResponse(
            {"error": "InvalidMongoURL", "error_description": "The provided MongoDB URL is not valid."},
            status_code=400,
        )

    if await test_db_connection(mongo_url) is False:
        return JSONResponse(
            {"error": "DatabaseConnectionFailed",
             "error_description": "Failed to connect to the database with the provided MongoDB URL. Check the logs for more information. Setup aborted."},
            status_code=400,
        )

    write_config("Global", "setup_complete", "true")
    write_config("Global", "instance_name", instance_name)
    write_config("Database", "MongoURL", mongo_url.strip())

    return JSONResponse({
        "success": True
    })
