from pydantic import BaseModel

from sqlalchemy import Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

    # table definitions
class AlertStateDB(Base):
    __tablename__ = "alert_states"

    alert_id: Mapped[str] = mapped_column(
        String,
        primary_key = True
    )

    seen: Mapped[bool] = mapped_column(
        Boolean,
        default = False,
        nullable = False
    )

    dismissed: Mapped[bool] = mapped_column(
        Boolean,
        default = False,
        nullable = False
    )

class AlertState(BaseModel):
    alert_id: str
    seen: bool = False
    dismissed: bool = False