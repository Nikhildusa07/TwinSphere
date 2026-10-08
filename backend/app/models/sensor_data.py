from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer

from app.db.database import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)

    digital_twin_id = Column(
        Integer,
        ForeignKey("digital_twins.id"),
        nullable=False,
    )

    temperature = Column(Float, nullable=False)
    vibration = Column(Float, nullable=False)
    power_usage = Column(Float, nullable=False)
    operating_speed = Column(Float, nullable=False)

    recorded_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )