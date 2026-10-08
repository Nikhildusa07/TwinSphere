from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DigitalTwinBase(BaseModel):
    name: str
    entity_type: str
    temperature: float | None = None
    vibration: float | None = None
    power_usage: float | None = None
    operating_speed: float | None = None
    status: str = "normal"


class DigitalTwinCreate(DigitalTwinBase):
    pass


class DigitalTwinResponse(DigitalTwinBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)