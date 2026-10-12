from fastapi import APIRouter

from backend.app.services.alert_service import get_active_alerts, mark_alert_seen, dismiss_alert

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status:" "ok"}


@router.get("/alerts")
async def alerts():
    return await get_active_alerts()

@router.post("/alerts/{alert_id}/seen")
def mark_seen(alert_id: str):
    return mark_alert_seen(alert_id)

@router.post("/alerts/{alert_id}/dismiss")
def dismiss(alert_id: str):
    return dismiss_alert(alert_id)

