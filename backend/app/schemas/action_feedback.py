from datetime import datetime

from pydantic import BaseModel


class ActionFeedbackCreate(BaseModel):
    digital_twin_id: int
    action: str
    predicted_temperature: float | None = None
    actual_temperature: float | None = None
    outcome: str


class ActionFeedbackResponse(ActionFeedbackCreate):
    id: int
    created_at: datetime