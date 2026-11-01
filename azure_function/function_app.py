import asyncio
import logging

import azure.functions as func

from services.refresh_service import refresh_alert_snapshot

app = func.FunctionApp()

@app.timer_trigger(
    schedule="%TIMER_SCHEDULE%",
    arg_name="timer",
    run_on_startup=False,
)

def refresh_alerts(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.warning("Alert refresh timer is running late")

    asyncio.run(refresh_alert_snapshot())

    logging.info("Alert snapshot refresh")