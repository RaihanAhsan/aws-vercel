from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SensorReadingIn(BaseModel):
    """Payload dari ESP32."""
    device_code: str = Field(..., min_length=1, max_length=50)
    wind_speed: Optional[float] = Field(None, ge=0, le=100)
    wind_direction: Optional[int] = Field(None, ge=0, le=360)
    temperature: Optional[float] = Field(None, ge=-40, le=80)
    humidity: Optional[float] = Field(None, ge=0, le=100)
    pressure: Optional[float] = Field(None, ge=300, le=1100)
    solar_radiation: Optional[int] = Field(None, ge=0, le=2000)
    rainfall: Optional[float] = Field(None, ge=0, le=500)


class SensorReadingOut(BaseModel):
    """Response dari API."""
    id: int
    device_code: str
    device_name: str
    wind_speed: Optional[float]
    wind_direction: Optional[int]
    temperature: Optional[float]
    humidity: Optional[float]
    pressure: Optional[float]
    solar_radiation: Optional[int]
    rainfall: Optional[float]
    created_at: datetime