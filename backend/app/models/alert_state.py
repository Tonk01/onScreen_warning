from pydantic import BaseModel

class AlertState(BaseModel):
    alert_id: str
    seen: bool = False
    dismissed: bool = False