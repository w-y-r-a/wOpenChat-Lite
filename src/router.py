from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates as TemplateResponse
import pathlib

TemplateResponse(
    directory=pathlib.Path(__file__).parent / "templates"
)

router = APIRouter(tags=["main"])


