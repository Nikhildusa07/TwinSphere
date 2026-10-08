from typing import Any

from sqlalchemy.orm import Session

from app.services.feedback_analysis_service import analyze_prediction_accuracy


def evaluate_learning_need(
    db: Session,
    retraining_threshold: float = 5.0,
) -> dict[str, Any]:
    """
    Evaluate stored prediction feedback and determine
    whether model retraining is recommended.
    """

    if retraining_threshold <= 0:
        raise ValueError(
            "Retraining threshold must be greater than zero."
        )

    analysis = analyze_prediction_accuracy(db)

    total_predictions = analysis["total_predictions"]
    average_error = analysis["average_error"]

    if total_predictions == 0:
        return {
            "retraining_required": False,
            "reason": "No prediction feedback is available.",
            "average_error": average_error,
            "total_predictions": total_predictions,
        }

    retraining_required = (
        average_error > retraining_threshold
    )

    if retraining_required:
        reason = (
            "Average prediction error exceeds the "
            "retraining threshold."
        )
    else:
        reason = (
            "Prediction performance is within the "
            "acceptable error threshold."
        )

    return {
        "retraining_required": retraining_required,
        "reason": reason,
        "average_error": average_error,
        "retraining_threshold": retraining_threshold,
        "total_predictions": total_predictions,
    }