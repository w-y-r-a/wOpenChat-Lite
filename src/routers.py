from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from settingsmanager import read_config
import pathlib

# Some config settings from settingsmanager
try:
    THEME_COLOR = read_config().get("customization").get("theme_color")
    FAVICON_URL = read_config().get("customization").get("favicon_url")
    setup_complete = read_config().get("global").get("setup_complete")
except AttributeError:
    THEME_COLOR = None
    FAVICON_URL = None
    setup_complete = None

templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent / "templates"
)

router = APIRouter(tags=["app"])

@router.get("/")
def root(request: Request):
    if not setup_complete:
        return templates.TemplateResponse("setup.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        })
    elif setup_complete:
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