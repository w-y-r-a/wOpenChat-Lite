from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import pathlib

templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent / "templates"
)

router = APIRouter(tags=["app"])

@router.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

