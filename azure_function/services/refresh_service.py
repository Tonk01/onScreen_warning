from services.entur_service import get_service_alerts
from services.azure_blob_service import upload_alert_snapshot

def validate_alerts(alerts) -> None:
    if alerts is None:
        raise ValueError("Entur returned no alert data")

    if not isinstance(alerts, list):
        raise ValueError("Entur response was not parsed in a list")

    for alert in alerts:
        if not alert.id:
            raise ValueError("Alert is missing an id")

async def refresh_alert_snapshot():
    alerts = await get_service_alerts()

    validate_alerts(alerts)

    await upload_alert_snapshot(alerts)
    return alerts