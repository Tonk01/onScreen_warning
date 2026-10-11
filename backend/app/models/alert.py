from datetime import datetime

from pydantic import BaseModel, Field

class Affects(BaseModel):
    lines: list[str] = Field(default_factory=list)
    stops: list[str] = Field(default_factory=list)
    journeys: list[str] = Field(default_factory=list)

class Alert(BaseModel):
    id: str
    creation_time: datetime | None = None
    status: str | None = None
    severity: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    summary: str | None = None
    description: str | None = None
    affects: Affects