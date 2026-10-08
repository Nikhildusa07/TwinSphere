from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.ml.train_model import train_prediction_model
from app.models.sensor_data import SensorData

from app.services.action_planning_service import create_action_plan
from app.services.anomaly_detection_service import detect_anomalies
from app.services.causal_analysis_service import analyze_causal_influence
from app.services.decision_engine_service import recommend_action
from app.services.prediction_service import prepare_prediction_features
from app.services.resource_allocation_service import allocate_resources
from app.services.risk_analysis_service import calculate_risk_level
from app.services.scenario_simulation_service import simulate_scenarios
from app.services.simulation_comparison_service import (
    compare_simulation_with_actual,
)
from app.services.simulation_service import simulate_future_state
from app.services.time_series_service import analyze_time_series
from app.services.reinforcement_learning_service import (
    select_best_action,
)


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post("/")
def predict_temperature(sensor_data: dict):
    """
    Predict the next temperature using the current
    sensor readings.
    """

    try:
        features = prepare_prediction_features(sensor_data)

        model = train_prediction_model()

        prediction = model.predict(features)

        return {
            "predicted_temperature": round(
                float(prediction[0]),
                2,
            ),
            "unit": "°C",
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.post("/anomaly")
def detect_sensor_anomaly(sensor_data: dict):
    """
    Detect abnormal sensor readings using
    operational thresholds.
    """

    required_fields = [
        "temperature",
        "vibration",
        "power_usage",
        "operating_speed",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in sensor_data
    ]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing sensor fields: {', '.join(missing_fields)}",
        )

    try:
        return detect_anomalies(sensor_data)

    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail="Sensor values must be numeric.",
        ) from error


@router.post("/risk")
def analyze_sensor_risk(sensor_data: dict):
    """
    Calculate the operational risk level based on
    current sensor conditions.
    """

    required_fields = [
        "temperature",
        "vibration",
        "power_usage",
        "operating_speed",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in sensor_data
    ]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing sensor fields: {', '.join(missing_fields)}",
        )

    try:
        return calculate_risk_level(sensor_data)

    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail="Sensor values must be numeric.",
        ) from error


@router.post("/causal-analysis")
def analyze_causal_relationships(
    digital_twin_id: int,
    db: Session = Depends(get_db),
):
    """
    Analyze historical sensor factors that influence
    digital-twin temperature.
    """

    records = (
        db.query(SensorData)
        .filter(
            SensorData.digital_twin_id == digital_twin_id
        )
        .order_by(SensorData.recorded_at.asc())
        .all()
    )

    if len(records) < 2:
        raise HTTPException(
            status_code=400,
            detail=(
                "At least 2 historical sensor records are "
                "required for causal analysis."
            ),
        )

    sensor_records = [
        {
            "temperature": record.temperature,
            "vibration": record.vibration,
            "power_usage": record.power_usage,
            "operating_speed": record.operating_speed,
        }
        for record in records
    ]

    try:
        return analyze_causal_influence(
            sensor_records
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.post("/time-series")
def analyze_temperature_time_series(
    digital_twin_id: int,
    db: Session = Depends(get_db),
):
    """
    Perform advanced time-series analysis on historical
    digital-twin temperature readings.
    """

    records = (
        db.query(SensorData)
        .filter(
            SensorData.digital_twin_id == digital_twin_id
        )
        .order_by(SensorData.recorded_at.asc())
        .all()
    )

    if len(records) < 3:
        raise HTTPException(
            status_code=400,
            detail=(
                "At least 3 historical sensor records are "
                "required for time-series analysis."
            ),
        )

    sensor_records = [
        {
            "temperature": record.temperature,
            "vibration": record.vibration,
            "power_usage": record.power_usage,
            "operating_speed": record.operating_speed,
        }
        for record in records
    ]

    try:
        return analyze_time_series(
            sensor_records
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.get("/simulation-vs-actual")
def compare_simulation_and_actual(
    db: Session = Depends(get_db),
):
    """
    Compare TwinSphere simulation/prediction results
    with actual operational outcomes.
    """

    return compare_simulation_with_actual(db)


@router.get("/reinforcement-learning")
def reinforcement_learning_recommendation(
    digital_twin_id: int,
    db: Session = Depends(get_db),
):
    """
    Select the best operational action using the
    reinforcement learning decision component.
    """

    twin = (
        db.query(SensorData)
        .filter(
            SensorData.digital_twin_id == digital_twin_id
        )
        .order_by(SensorData.recorded_at.desc())
        .first()
    )

    if not twin:
        raise HTTPException(
            status_code=404,
            detail=(
                "No sensor data found for the specified "
                "digital twin."
            ),
        )

    try:
        return select_best_action(
            temperature=twin.temperature,
            vibration=twin.vibration,
            power_usage=twin.power_usage,
            operating_speed=twin.operating_speed,
        )

    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.post("/simulate")
def simulate_sensor_state(
    sensor_data: dict,
    temperature_change: float = 0.0,
    vibration_change: float = 0.0,
    power_usage_change: float = 0.0,
    operating_speed_change: float = 0.0,
):
    """
    Simulate a future digital-twin state by applying
    user-defined changes to the current sensor state.
    """

    required_fields = [
        "temperature",
        "vibration",
        "power_usage",
        "operating_speed",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in sensor_data
    ]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing sensor fields: {', '.join(missing_fields)}",
        )

    try:
        return simulate_future_state(
            sensor_data=sensor_data,
            temperature_change=temperature_change,
            vibration_change=vibration_change,
            power_usage_change=power_usage_change,
            operating_speed_change=operating_speed_change,
        )

    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail="Sensor values and simulation changes must be numeric.",
        ) from error


@router.post("/scenarios")
def simulate_multiple_scenarios(
    sensor_data: dict,
    scenarios: list[dict],
):
    """
    Simulate multiple possible future states and
    calculate the risk level for each scenario.
    """

    required_fields = [
        "temperature",
        "vibration",
        "power_usage",
        "operating_speed",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in sensor_data
    ]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing sensor fields: {', '.join(missing_fields)}",
        )

    if not scenarios:
        raise HTTPException(
            status_code=400,
            detail="At least one scenario is required.",
        )

    try:
        return {
            "scenario_count": len(scenarios),
            "results": simulate_scenarios(
                sensor_data=sensor_data,
                scenarios=scenarios,
            ),
        }

    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail="Sensor values and scenario changes must be numeric.",
        ) from error


@router.post("/decision")
def make_decision(
    scenario_results: list[dict],
):
    """
    Select the safest scenario and recommend
    an operational action.
    """

    if not scenario_results:
        raise HTTPException(
            status_code=400,
            detail="At least one scenario result is required.",
        )

    try:
        return recommend_action(scenario_results)

    except (TypeError, ValueError, KeyError) as error:
        raise HTTPException(
            status_code=400,
            detail="Invalid scenario results.",
        ) from error


@router.post("/resource-allocation")
def allocate_operational_resources(
    risk_level: str,
    current_load: float,
):
    """
    Recommend resource allocation based on the
    current operational risk and system load.
    """

    try:
        return allocate_resources(
            risk_level=risk_level,
            current_load=current_load,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.post("/action-plan")
def generate_action_plan(
    risk_level: str,
    recommended_action: str,
    resource_allocation: dict,
):
    """
    Generate an autonomous operational action plan
    using risk, recommended action, and resource allocation.
    """

    try:
        return create_action_plan(
            risk_level=risk_level,
            recommended_action=recommended_action,
            resource_allocation=resource_allocation,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error