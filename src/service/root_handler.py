from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from src.settingsmanager import read_config
from src.utils.database import get_collection
import pathlib

try:
    THEME_COLOR = read_config().get("customization").get("theme_color") # pyright: ignore[reportOptionalMemberAccess]
except AttributeError:
    THEME_COLOR = None
try:
    FAVICON_URL = read_config().get("customization").get("favicon_url") # pyright: ignore[reportOptionalMemberAccess]
except AttributeError:
    FAVICON_URL = None

async def root_handler(request: Request, response: Response):
    """
    Handle the root endpoint and return a welcome message with configuration details.

    Args:
        request (Request): The incoming request object.
        response (Response): The outgoing response object.

    Returns:
        JSONResponse: A JSON response containing a welcome message and configuration details.
    """
    tokens = await get_collection("tokens")
    sid = request.cookies.get("session_token")
    if sid:
        token = await tokens.find_one({"session_token": sid})
    else:
        token = None # TODO: make it redirect to login if no token found, but actually make the login
    # lowk ill just do this later, gotta make the login system first