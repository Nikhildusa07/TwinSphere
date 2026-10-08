from typing import Any

from sqlalchemy.orm import Session

from app.models.action_feedback import ActionFeedback


def analyze_prediction_accuracy(
    db: Session,
) -> dict[str, Any]:
    """
    Analyze prediction accuracy using stored action feedback.
    """

    feedback_records = (
        db.query(ActionFeedback)
        .filter(
            ActionFeedback.predicted_temperature.isnot(None),
            ActionFeedback.actual_temperature.isnot(None),
        )
        .all()
    )

    if not feedback_records:
        return {
            "total_predictions": 0,
            "average_error": 0.0,
            "accurate_predictions": 0,
            "acceptable_predictions": 0,
            "inaccurate_predictions": 0,
            "accuracy_rate": 0.0,
        }

    errors = []

    accurate_predictions = 0
    acceptable_predictions = 0
    inaccurate_predictions = 0

    for record in feedback_records:
        error = abs(
            record.predicted_temperature
            - record.actual_temperature
        )

        errors.append(error)

        if error <= 2:
            accurate_predictions += 1
        elif error <= 5:
            acceptable_predictions += 1
        else:
            inaccurate_predictions += 1

    total_predictions = len(feedback_records)

    average_error = sum(errors) / total_predictions

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
    }