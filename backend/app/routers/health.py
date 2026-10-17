from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.health import ReadinessResponse
from app.interfaces.health_service import IHealthCheck
from app.core.dependencies import get_session, get_health_service


router = APIRouter(prefix="/health", tags=["System"])

@router.get("/liveness")
def liveness_check():
    """**後端存活檢查**

    檢查後端是否還活著，應用排程器每幾秒call一下
    """
    return {"status": "ok", "service": "up"}

@router.get("/readiness", response_model=ReadinessResponse)
def readiness_check(
        db: Session = Depends(get_session), 
        HealthCheckService: IHealthCheck = Depends(get_health_service)
    ):
    """**系統就緒檢查**
    
    檢查應用程式是否已準備好接收流量(例如:資料庫連線是否正常)\n
    要用外部應用排程器每幾秒call一下\n
    若有元件異常，將回傳 503 狀態碼
    """
    return HealthCheckService.check_readiness(db)