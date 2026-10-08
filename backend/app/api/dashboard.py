from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.digital_twin import DigitalTwin
from app.models.sensor_data import SensorData
from app.services.continuous_learning_service import evaluate_learning_need
from app.services.risk_analysis_service import calculate_risk_level


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/overview")
def get_dashboard_overview(
    db: Session = Depends(get_db),
):
    """
    Return the main TwinSphere dashboard information.
    """

    twin = (
        db.query(DigitalTwin)
        .order_by(DigitalTwin.updated_at.desc())
        .first()
    )

    if twin is None:
        raise HTTPException(
            status_code=404,
            detail="No digital twin is available.",
        )

    latest_sensor_data = (
        db.query(SensorData)
        .filter(
            SensorData.digital_twin_id == twin.id
        )
        .order_by(SensorData.recorded_at.desc())
        .first()
    )

    if latest_sensor_data is None:
        sensor_state = {
            "temperature": twin.temperature,
            "vibration": twin.vibration,
            "power_usage": twin.power_usage,
            "operating_speed": twin.operating_speed,
        }
    else:
        sensor_state = {
            "temperature": latest_sensor_data.temperature,
            "vibration": latest_sensor_data.vibration,
            "power_usage": latest_sensor_data.power_usage,
            "operating_speed": latest_sensor_data.operating_speed,
        }

    if all(
        value is not None
        for value in sensor_state.values()
    ):
        risk = calculate_risk_level(sensor_state)
    else:
        risk = {
            "risk_score": 0,
            "risk_level": "unknown",
            "risk_factors": [],
        }

    learning_status = evaluate_learning_need(db)

    return {
        "digital_twin": {
            "id": twin.id,
            "name": twin.name,
            "entity_type": twin.entity_type,
            "status": twin.status,
        },
        "current_state": sensor_state,
        "risk": risk,
        "learning_status": learning_status,
    }