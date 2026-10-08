from datetime import datetime

from pydantic import BaseModel


class SensorDataCreate(BaseModel):
    digital_twin_id: int
    temperature: float
    vibration: float
    power_usage: float
    operating_speed: float


class SensorDataResponse(SensorDataCreate):
    id: int
    recorded_at: datetime