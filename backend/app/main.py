from fastapi import FastAPI

from backend.app.api.routes import router
from backend.app.database import init_db

app = FastAPI()

init_db()

app.include_router(router)

@app.get("/")
def root():
    return {"Message: Ado is the best"}