from services.entur_service import get_service_alerts
from services.azure_blob_service import upload_alert_snapshot

async def refresh_alert_snapshot():
    alerts = await get_service_alerts()

    await upload_alert_snapshot(alerts)
    return alerts