from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import pathlib
import os
import sys
sys.path.insert(1, os.getcwd())
from service import root_handler
from utils.config import get_customization_config

config = get_customization_config()
THEME_COLOR = config["theme_color"]
FAVICON_URL = config["favicon_url"]
setup_complete = config["setup_complete"]

templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent / "templates"
)

router = APIRouter(tags=["app"])

@router.get("/")
async def root(request: Request, response: Response):
    if setup_complete:
        return await root_handler.root_handler(request, response)
    else:
        return templates.TemplateResponse("setup.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        })