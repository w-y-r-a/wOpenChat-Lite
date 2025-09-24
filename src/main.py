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
from settingsmanager import read_config
from routers import router
from apis import api
import pathlib
logger = logging.getLogger(__name__)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    basically startup scripts
    """
    print("\033[32mINFO\033[0m:     Starting wOpenChat Lite...")
    yield
    print("\033[32mINFO\033[0m:     Stopping wOpenChat Lite...")

app = FastAPI(
    title="wOpenChat Lite",
    version=getenv("VERSION", "1.0.0"), # set during build process in the CI/CD Pipeline(gh actions)
    lifespan=lifespan
)

THEME_COLOR = read_config("Customization", "theme_color")
FAVICON_URL = read_config("Customization", "favicon_url")

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

app.include_router(router)
app.include_router(api, prefix="/api")

uvicorn.run(
    app, 
    host="0.0.0.0"
)