from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import pathlib
import os
import sys
sys.path.insert(1, os.getcwd())
from service import root_handler
from settingsmanager import read_config

try:
    THEME_COLOR = read_config().get("customization").get("theme_color") # pyright: ignore[reportOptionalMemberAccess]
except (AttributeError, KeyError, TypeError):
    THEME_COLOR = None
try:
    FAVICON_URL = read_config().get("customization").get("favicon_url") # pyright: ignore[reportOptionalMemberAccess]
except (AttributeError, KeyError, TypeError):
    FAVICON_URL = None
try:
    setup_complete = read_config().get("global").get("setup_complete") # pyright: ignore[reportOptionalMemberAccess]
except (AttributeError, KeyError, TypeError):
    setup_complete = False

templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent / "templates"
)

router = APIRouter(tags=["app"])

@router.get("/")
async def root(request: Request, response: Response):
    if setup_complete == True:
        return await root_handler.root_handler(request, response)
    else:
        return templates.TemplateResponse("setup.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        })