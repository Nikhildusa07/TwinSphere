from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.db.database import Base


class ActionFeedback(Base):
    __tablename__ = "action_feedback"

    id = Column(Integer, primary_key=True, index=True)

    digital_twin_id = Column(
        Integer,
        nullable=False,
    )

    action = Column(
        String(255),
        nullable=False,
    )

    predicted_temperature = Column(
        Float,
        nullable=True,
    )

    actual_temperature = Column(
        Float,
        nullable=True,
    )

    outcome = Column(
        String(100),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )