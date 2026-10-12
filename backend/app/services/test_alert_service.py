from datetime import datetime, timedelta

from backend.app.models.alert import Alert, Affects

# temporary for testing. 
def get_test_alert() -> list[Alert]:
    now = datetime.now().astimezone()

    return [
        Alert(
            id="TEST:1",
            creation_time=now,
            status="open",
            severity="normal",
            start_time=now - timedelta(minutes=10),
            end_time=now + timedelta(hours=2),
            summary="Test alert 1",
            description="Bus route 10 is delayed.",
            affects=Affects(
                lines=["TEST:Line:10"]
            )
        ),

        Alert(
            id="TEST:2",
            creation_time=now,
            status="open",
            severity="normal",
            start_time=now - timedelta(minutes=5),
            end_time=now + timedelta(hours=1),
            summary="Test alert 2",
            description="Tram route 2 is temporarily stopped.",
            affects=Affects(
                lines=["TEST:Line:2"]
            )
        ),

        Alert(
            id="TEST:3",
            creation_time=now,
            status="open",
            severity="normal",
            start_time=now - timedelta(minutes=30),
            end_time=now + timedelta(hours=3),
            summary="Test alert 3",
            description="Roadworks are affecting several stops.",
            affects=Affects(
                lines=["TEST:Line:20"],
                stops=[
                    "TEST:Stop:1",
                    "TEST:Stop:2"
                ]
            )
        )
    ]