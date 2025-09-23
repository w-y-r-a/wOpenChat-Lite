from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
from os import getenv
import logging
import settingsmanager
from routers import router
from api import router as apirouters
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

app.mount("/static", StaticFiles(directory=pathlib.Path(__file__).parent / "static"), name="static")

app.include_router(router)
app.include_router(apirouters, prefix="/api")

uvicorn.run(
    app, 
    host="0.0.0.0"
)