from datetime import datetime 


from backend.app.services.entur_service import get_service_alerts
from backend.app.services.test_alert_service import get_test_alert

from backend.app.database import SessionLocal
from backend.app.models.alert_state import AlertStateDB, AlertState

    # get or create alertstate from the db.
def get_alert_state(alert_id: str) -> AlertState:
    with SessionLocal() as db:
        state_db = db.get(AlertStateDB, alert_id)

        if state_db is None:
            state_db = AlertStateDB(
                alert_id = alert_id,
                seen = False,
                dismissed = False
            )

            db.add(state_db)
            db.commit()
            db.refresh(state_db)

        return AlertState(
            alert_id = state_db.alert_id,
            seen = state_db.seen,
            dismissed = state_db.dismissed
        )

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

    # self-explan
def mark_alert_seen(alert_id: str) -> AlertState:
    with SessionLocal() as db:
        state_db = db.get(AlertStateDB, alert_id)

        if state_db is None:
            state_db = AlertStateDB(
                alert_id = alert_id,
                seen = True,
                dismissed = False
            )

            db.add(state_db)
        else: 
            state_db.seen = True

        db.commit()
        db.refresh(state_db)

        return AlertState(
            alert_id = state_db.alert_id,
            seen = state_db.seen,
            dismissed = state_db.dismissed
        )

    # self-explan
def dismiss_alert(alert_id: str) -> AlertState:
    with SessionLocal() as db:
        state_db = db.get(AlertStateDB, alert_id)

        if state_db is None:
            state_db = AlertStateDB(
                alert_id = alert_id,
                seen = False,
                dismissed = True
            )

            db.add(state_db)
        else:
            state_db.seen = True
            state_db.dismissed = True

        db.commit()
        db.refresh(state_db)

        return AlertState(
            alert_id = state_db.alert_id,
            seen = state_db.seen,
            dismissed = state_db.dismissed
        )

def restore_alert(alert_id: str) -> AlertState:
    with SessionLocal() as db:
        state_db = db.get(AlertStateDB, alert_id)

        if state_db is None:
            state_db = AlertStateDB(
                alert_id = alert_id,
                seen = False,
                dismissed = False
            )

            db.add(state_db)
        else:
            state_db.dismissed = False

        db.commit()
        db.refresh(state_db)

        return AlertState(
            alert_id = state_db.alert_id,
            seen = state_db.seen,
            dismissed = state_db.dismissed
        )

async def get_dismissed_alerts():
    alerts = await get_service_alerts()
    now = datetime.now().astimezone()

    dismissed_alerts = []

    for alert in alerts:
        if not alert.is_active(now):
            continue

        state = get_alert_state(alert.id)

        if not state.dismissed:
            continue

        dismissed_alerts.append(alert)

    return dismissed_alerts

    # temporary for test cases. 
async def get_active_test_alerts():
    alerts = get_test_alert()

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