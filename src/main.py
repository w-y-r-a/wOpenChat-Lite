from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
from os import getenv
import logging
from datetime import datetime, timedelta, timezone
logger = logging.getLogger(f"   {datetime.now}:")

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

@app.get("/")
def root():
    """
    lit just the root
    """
    return {
        "status": "healthy",
        "service": "wOpenChat",
        "edition": "lite",
        "version": app.version
    }

uvicorn.run(
    app, 
    host="0.0.0.0"
)