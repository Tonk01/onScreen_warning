from fastapi import APIRouter

from backend.app.services.alert_service import (
    get_active_alerts, 
    mark_alert_seen, 
    dismiss_alert, 
    get_dismissed_alerts, 
    restore_alert
)

from backend.app.models.alert_state import AlertState
from backend.app.models.alert import Alert

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status:" "ok"}

@router.get("/alerts", response_model = list[Alert])
async def alerts():
    return await get_active_alerts()

@router.get("/alerts/dismissed")
async def dismissed_alerts():
    return await get_dismissed_alerts()


@router.post("/alerts/{alert_id}/seen", response_model = AlertState)
def mark_seen(alert_id: str):
    return mark_alert_seen(alert_id)

@router.post("/alerts/{alert_id}/dismiss", response_model = AlertState)
def dismiss(alert_id: str):
    return dismiss_alert(alert_id)

@router.post("/alerts/{alert_id}/restore")
def restore(alert_id: str):
    return restore_alert(alert_id)