from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.db.database import Base


class DigitalTwin(Base):
    __tablename__ = "digital_twins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)

    temperature = Column(Float, nullable=True)
    vibration = Column(Float, nullable=True)
    power_usage = Column(Float, nullable=True)
    operating_speed = Column(Float, nullable=True)

    status = Column(String(50), default="normal", nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )