from fastapi import APIRouter

from app.routers.health import router as health_router
from app.routers.stock import router as stock_router


router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(stock_router)