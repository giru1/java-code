from fastapi import APIRouter
from app import app
from wallets.router import router as router_wallets

app_router = APIRouter(prefix="/api/v1")
app_router.include_router(router_wallets)
app.include_router(app_router)
