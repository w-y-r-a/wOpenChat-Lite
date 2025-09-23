from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from os import getenv

load_dotenv()

api = APIRouter(tags=["api"])

@api.get("/health")
def healthcheck():
    return {
        "status": "healthy",
        "edition": "lite",
        "version": getenv("VERSION", "1.0.0"), # set during build process in the CI/CD Pipeline(gh actions)
    }