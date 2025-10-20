import time
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
from os import getenv
import logging
import pathlib
import os
import sys
sys.path.insert(1, os.getcwd())
from src.settingsmanager import read_config, ensure_config, write_config
from src.utils.database import init_db, close_db_connection
from src.utils.ensure_indexes import ensure_indexes
logger = logging.getLogger(__name__)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    basically startup scripts
    """
    print("\033[32mINFO\033[0m:     Starting wOpenChat Lite...")
    await ensure_config()
    global THEME_COLOR, FAVICON_URL
    try:
        THEME_COLOR = read_config().get("customization").get("theme_color") # pyright: ignore[reportOptionalMemberAccess]
    except AttributeError:
        THEME_COLOR = None
    try:
        FAVICON_URL = read_config().get("customization").get("favicon_url") # pyright: ignore[reportOptionalMemberAccess]
    except AttributeError:
        FAVICON_URL = None
    await init_db()
    await ensure_indexes()
    from src.routers import router
    from src.apis import api
    app.include_router(router)
    app.include_router(api, prefix="/api")
    try:
        yield
        print("\033[32mINFO\033[0m:     Stopping wOpenChat Lite...")
    finally:
        close_db_connection()
        print("\033[32mINFO\033[0m:     Stopped wOpenChat Lite.")

app = FastAPI(
    title="wOpenChat Lite",
    version=getenv("VERSION", "1.0.0"), # set during build process in the CI/CD Pipeline(gh actions)
    lifespan=lifespan
)

templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent / "templates" / "errors"
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        }, status_code=404)
    return await http_exception_handler(request, exc)

app.mount("/static", StaticFiles(directory=pathlib.Path(__file__).parent / "static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0"
    )