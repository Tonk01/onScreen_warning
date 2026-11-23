from fastapi import APIRouter, Response

from backend.app.models.alert import Alert
from backend.app.services.alert_service import get_active_alerts


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/alerts", response_model=list[Alert])
async def alerts(response: Response):
    alerts, last_modified = await get_active_alerts()

    response.headers["Last-Modified"] = last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")

    return alerts