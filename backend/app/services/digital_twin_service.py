from sqlalchemy.orm import Session

from app.models.digital_twin import DigitalTwin
from app.models.sensor_data import SensorData


def update_digital_twin_state(
    db: Session,
    sensor_data: SensorData,
) -> DigitalTwin | None:
    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.id == sensor_data.digital_twin_id)
        .first()
    )

    if twin is None:
        return None

    twin.temperature = sensor_data.temperature
    twin.vibration = sensor_data.vibration
    twin.power_usage = sensor_data.power_usage
    twin.operating_speed = sensor_data.operating_speed

    db.commit()
    db.refresh(twin)

    return twin