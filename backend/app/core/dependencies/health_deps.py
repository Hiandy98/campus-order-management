from app.interfaces.health_service import IHealthCheck
from app.services.health import HealthCheckService

def get_health_service() -> IHealthCheck:
    return HealthCheckService()