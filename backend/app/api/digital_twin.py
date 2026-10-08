from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.digital_twin import DigitalTwin
from app.schemas.digital_twin import DigitalTwinCreate, DigitalTwinResponse


router = APIRouter(
    prefix="/digital-twins",
    tags=["Digital Twins"],
)


@router.post(
    "/",
    response_model=DigitalTwinResponse,
)
def create_digital_twin(
    twin: DigitalTwinCreate,
    db: Session = Depends(get_db),
):
    new_twin = DigitalTwin(
        name=twin.name,
        entity_type=twin.entity_type,
        temperature=twin.temperature,
        vibration=twin.vibration,
        power_usage=twin.power_usage,
        operating_speed=twin.operating_speed,
        status=twin.status,
    )

    db.add(new_twin)
    db.commit()
    db.refresh(new_twin)

    return new_twin


@router.get(
    "/",
    response_model=list[DigitalTwinResponse],
)
def get_digital_twins(
    db: Session = Depends(get_db),
):
    return db.query(DigitalTwin).all()