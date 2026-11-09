from datetime import datetime 

from backend.app.models.alert import Alert
from backend.app.services.azure_blob_service import get_alert_snapshot

    # gets active alerts from blob storage snapshot
async def get_active_alerts() -> list[Alert]:
    snapshot = await get_alert_snapshot()

    alerts = [
        Alert(**alert_data) 
        for alert_data in snapshot["alerts"]
    ]

    now = datetime.now().astimezone()

    active_alerts = []

    for alert in alerts:
        if not alert.is_active(now):
            continue

        active_alerts.append(alert)

    return active_alerts