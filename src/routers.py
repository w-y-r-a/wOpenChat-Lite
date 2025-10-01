from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from settingsmanager import read_config
import pathlib

try:
    THEME_COLOR = read_config().get("customization").get("theme_color")
except AttributeError:
    THEME_COLOR = None
try:
    FAVICON_URL = read_config().get("customization").get("favicon_url")
except:
    FAVICON_URL = None
try:
    setup_complete = read_config().get("global").get("setup_complete") # pyright: ignore[reportOptionalMemberAccess]
except:
    setup_complete = False

templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent / "templates"
)

router = APIRouter(tags=["app"])

@router.get("/")
def root(request: Request):
    if setup_complete == False:
        print(1)
        print(setup_complete)
        return templates.TemplateResponse("setup.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        })
    elif setup_complete == True:
        print(2)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        })
    else:
        print(3)
        return templates.TemplateResponse("setup.html", {
            "request": request,
            "THEME_COLOR": THEME_COLOR,
            "FAVICON_URL": FAVICON_URL
        })