from fastapi import APIRouter, Response

from backend.app.services.entur_service import get_service_alerts

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status:" "ok"}


@router.get("/alerts")
async def alerts():
    return await get_service_alerts()

