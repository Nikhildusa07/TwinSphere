from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.digital_twin import DigitalTwin
from app.models.sensor_data import SensorData
from app.schemas.sensor_data import SensorDataCreate, SensorDataResponse
from app.services.data_processing_service import process_sensor_data
from app.services.digital_twin_service import update_digital_twin_state


router = APIRouter(
    prefix="/sensor-data",
    tags=["Sensor Data"],
)


@router.post(
    "/",
    response_model=SensorDataResponse,
)
def create_sensor_data(
    sensor_data: SensorDataCreate,
    db: Session = Depends(get_db),
):
    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.id == sensor_data.digital_twin_id)
        .first()
    )

    if twin is None:
        raise HTTPException(
            status_code=404,
            detail="Digital twin not found",
        )

    raw_sensor_data = sensor_data.model_dump()

    try:
        processed_sensor_data = process_sensor_data(
            raw_sensor_data
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    new_sensor_data = SensorData(
        digital_twin_id=processed_sensor_data["digital_twin_id"],
        temperature=processed_sensor_data["temperature"],
        vibration=processed_sensor_data["vibration"],
        power_usage=processed_sensor_data["power_usage"],
        operating_speed=processed_sensor_data["operating_speed"],
    )

    db.add(new_sensor_data)
    db.commit()
    db.refresh(new_sensor_data)

    update_digital_twin_state(
        db,
        new_sensor_data,
    )

    return new_sensor_data


@router.get(
    "/",
    response_model=list[SensorDataResponse],
)
def get_sensor_data(
    db: Session = Depends(get_db),
):
    return db.query(SensorData).all()