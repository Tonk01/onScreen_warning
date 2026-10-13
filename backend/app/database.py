from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models.alert_state import Base

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "onscreen.db"

DATABASE_PATH.parent.mkdir(parents = True, exist_ok = True)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine,
)

    # Base connection to database engine. 
def init_db(): 
    Base.metadata.create_all(bind = engine)