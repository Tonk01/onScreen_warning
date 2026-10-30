from fastapi import APIRouter

from backend.app.models.alert import Alert
from backend.app.services.azure_blob_service import get_alert_snapshot, upload_alert_snapshot
from backend.app.services.alert_service import get_active_alerts


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/alerts", response_model=list[Alert])
async def alerts():
    return await get_active_alerts()

@router.get("/azure_test")
async def azure_test():
    return await get_alert_snapshot()




@router.post("/azure-test/upload")
async def azure_upload_test():
    alerts = await get_active_alerts()

    await upload_alert_snapshot(alerts)

    return {
        "status": "uploaded",
        "count": len(alerts)
    }