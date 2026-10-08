from typing import Any

from sqlalchemy.orm import Session

from app.ml.train_model import train_prediction_model
from app.models.action_feedback import ActionFeedback
from app.models.sensor_data import SensorData
from app.services.prediction_service import (
    prepare_prediction_features,
)


def analyze_prediction_accuracy(
    db: Session,
) -> dict[str, Any]:
    """
    Analyze prediction accuracy.

    First, use stored action feedback records when available.

    If no evaluated feedback records exist, evaluate the
    prediction model against consecutive historical sensor
    readings. Each previous sensor reading is used to predict
    the next recorded temperature.
    """

    feedback_records = (
        db.query(ActionFeedback)
        .filter(
            ActionFeedback.predicted_temperature.isnot(None),
            ActionFeedback.actual_temperature.isnot(None),
        )
        .all()
    )

    if feedback_records:
        return _calculate_feedback_accuracy(
            feedback_records
        )

    return _calculate_historical_prediction_accuracy(db)


def _calculate_feedback_accuracy(
    feedback_records: list[ActionFeedback],
) -> dict[str, Any]:
    """
    Calculate prediction accuracy from stored feedback records.
    """

    errors = []

    accurate_predictions = 0
    acceptable_predictions = 0
    inaccurate_predictions = 0

    for record in feedback_records:
        error = abs(
            float(record.predicted_temperature)
            - float(record.actual_temperature)
        )

        errors.append(error)

        if error <= 2:
            accurate_predictions += 1
        elif error <= 5:
            acceptable_predictions += 1
        else:
            inaccurate_predictions += 1

    total_predictions = len(feedback_records)

    average_error = (
        sum(errors) / total_predictions
    )

    accuracy_rate = (
        accurate_predictions / total_predictions
    ) * 100

    return {
        "total_predictions": total_predictions,
        "average_error": round(average_error, 2),
        "accurate_predictions": accurate_predictions,
        "acceptable_predictions": acceptable_predictions,
        "inaccurate_predictions": inaccurate_predictions,
        "accuracy_rate": round(accuracy_rate, 2),
        "evaluation_source": "stored_feedback",
    }


def _calculate_historical_prediction_accuracy(
    db: Session,
) -> dict[str, Any]:
    """
    Evaluate one-step temperature predictions against
    consecutive historical sensor records.

    Example:

        Record 1 sensor state
                ↓
        Predict Record 2 temperature
                ↓
        Compare with Record 2 actual temperature

    This provides a real historical model evaluation even
    when no ActionFeedback records have been submitted yet.
    """

    records = (
        db.query(SensorData)
        .order_by(
            SensorData.digital_twin_id.asc(),
            SensorData.recorded_at.asc(),
        )
        .all()
    )

    if len(records) < 2:
        return {
            "total_predictions": 0,
            "average_error": 0.0,
            "accurate_predictions": 0,
            "acceptable_predictions": 0,
            "inaccurate_predictions": 0,
            "accuracy_rate": 0.0,
            "evaluation_source": "historical_sensor_data",
        }

    try:
        model = train_prediction_model()
    except (ValueError, TypeError):
        return {
            "total_predictions": 0,
            "average_error": 0.0,
            "accurate_predictions": 0,
            "acceptable_predictions": 0,
            "inaccurate_predictions": 0,
            "accuracy_rate": 0.0,
            "evaluation_source": "historical_sensor_data",
        }

    errors = []

    accurate_predictions = 0
    acceptable_predictions = 0
    inaccurate_predictions = 0

    predictions_evaluated = 0

    for index in range(len(records) - 1):
        current_record = records[index]
        next_record = records[index + 1]

        if (
            current_record.digital_twin_id
            != next_record.digital_twin_id
        ):
            continue

        sensor_data = {
            "temperature": current_record.temperature,
            "vibration": current_record.vibration,
            "power_usage": current_record.power_usage,
            "operating_speed": current_record.operating_speed,
        }

        try:
            features = prepare_prediction_features(
                sensor_data
            )

            prediction = model.predict(features)

            predicted_temperature = float(
                prediction[0]
            )

            actual_temperature = float(
                next_record.temperature
            )

            error = abs(
                predicted_temperature
                - actual_temperature
            )

            errors.append(error)
            predictions_evaluated += 1

            if error <= 2:
                accurate_predictions += 1
            elif error <= 5:
                acceptable_predictions += 1
            else:
                inaccurate_predictions += 1

        except (
            TypeError,
            ValueError,
            KeyError,
        ):
            continue

    if predictions_evaluated == 0:
        return {
            "total_predictions": 0,
            "average_error": 0.0,
            "accurate_predictions": 0,
            "acceptable_predictions": 0,
            "inaccurate_predictions": 0,
            "accuracy_rate": 0.0,
            "evaluation_source": "historical_sensor_data",
        }

    average_error = (
        sum(errors) / predictions_evaluated
    )

    accuracy_rate = (
        accurate_predictions
        / predictions_evaluated
    ) * 100

    return {
        "total_predictions": predictions_evaluated,
        "average_error": round(
            average_error,
            2,
        ),
        "accurate_predictions": accurate_predictions,
        "acceptable_predictions": acceptable_predictions,
        "inaccurate_predictions": inaccurate_predictions,
        "accuracy_rate": round(
            accuracy_rate,
            2,
        ),
        "evaluation_source": "historical_sensor_data",
    }