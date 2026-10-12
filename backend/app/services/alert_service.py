from datetime import datetime 

from backend.app.models.alert_state import AlertState
from backend.app.services.entur_service import get_service_alerts

alert_states: dict [str, AlertState] = {}

async def get_active_alerts():
    alerts = await get_service_alerts()

    now = datetime.now().astimezone()

    visible_alerts = []

    for alert in alerts: 
        if not alert.is_active(now):
            continue

        state = get_alert_state(alert.id)

        if state.dismissed:
            continue

        visible_alerts.append(alert)

        return visible_alerts


    # get or create an AlertState
def get_alert_state(alert_id: str) -> AlertState:
    if alert_id not in alert_states:
        alert_states[alert_id] = AlertState(alert_id = alert_id)

    return alert_states[alert_id]

    # self-explan
def mark_alert_seen(alert_id: str) -> AlertState:
    state = get_alert_state(alert_id)
    state.seen = True

    return state

    # self-explan
def dismiss_alert(alert_id: str) -> AlertState:
    state = get_alert_state(alert_id)
    state.dismissed = True

    return state