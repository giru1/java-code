import asyncio
import time
from pprint import pprint
# from urllib.request import Request
import json
from fastapi import APIRouter, FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

from wallets.router import router as router_wallets

from config import settings


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


app = App(title="Wallets Module", version="0.1")
app_router = APIRouter(prefix="/api/v1")
app_router.include_router(router_wallets)


app.include_router(app_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS.split(";"),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)