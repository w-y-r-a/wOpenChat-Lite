from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from settingsmanager import read_config
import pathlib

# Some config settings from settingsmanager
THEME_COLOR = read_config("Customization", "theme_color")
FAVICON_URL = read_config("Customization", "favicon_url")

templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent / "templates"
)

router = APIRouter(tags=["app"])

@router.get("/")
def root(request: Request):
    if read_config("Global", "setup_complete") is None:
        return templates.TemplateResponse("setup.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        })
    elif read_config("Global", "setup_complete"):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        })
    else:
        return templates.TemplateResponse("setup.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        })