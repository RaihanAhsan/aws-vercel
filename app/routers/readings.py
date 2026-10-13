from fastapi import APIRouter, HTTPException, Header, Query
from app.schemas import SensorReadingIn
from app import models

router = APIRouter(prefix="/api/readings", tags=["Readings"])


@router.post("")
def terima_data(
    payload: SensorReadingIn,
    x_api_key: str = Header(..., alias="X-API-Key"),
):
    """Terima data dari ESP32 (butuh header X-API-Key)."""
    device = models.get_device_by_code(payload.device_code)
    if not device:
        raise HTTPException(404, "Device tidak terdaftar")
    if not device["is_active"]:
        raise HTTPException(403, "Device tidak aktif")
    if device["api_key"] != x_api_key:
        raise HTTPException(401, "API key salah")

    data = payload.model_dump(exclude={"device_code"})
    reading_id = models.insert_reading(device["id"], data)

    return {"status": "ok", "id": reading_id, "message": "Data tersimpan"}


@router.get("/latest")
def latest(device_code: str = Query("STATION-01")):
    row = models.get_latest(device_code)
    if not row:
        raise HTTPException(404, "Belum ada data")
    row["created_at"] = row["created_at"].isoformat()
    return row


@router.get("/history")
def history(
    device_code: str = Query("STATION-01"),
    sensor: str = Query("wind_speed"),
    limit: int = Query(30, ge=1, le=200),
):
    try:
        rows = models.get_history(device_code, sensor, limit)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return [
        {"value": r["value"], "created_at": r["created_at"].isoformat()}
        for r in rows
    ]


@router.get("/stats")
def stats(
    device_code: str = Query("STATION-01"),
    sensor: str = Query("wind_speed"),
):
    try:
        row = models.get_stats(device_code, sensor)
    except ValueError as e:
        raise HTTPException(400, str(e))
    if not row:
        raise HTTPException(404, "Belum ada data")
    return row