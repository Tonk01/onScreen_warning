from fastapi import APIRouter

from backend.app.models.alert import Alert
from backend.app.services.alert_service import get_active_alerts


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/alerts", response_model=list[Alert])
async def alerts():
    return await get_active_alerts()