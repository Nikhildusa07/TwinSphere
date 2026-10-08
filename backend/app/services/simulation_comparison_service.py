from typing import Any

from sqlalchemy.orm import Session

from app.models.action_feedback import ActionFeedback


def compare_simulation_with_actual(
    db: Session,
) -> dict[str, Any]:
    """
    Compare predicted temperatures with actual temperatures
    stored in action feedback records.
    """

    records = (
        db.query(ActionFeedback)
        .filter(
            ActionFeedback.predicted_temperature.isnot(None),
            ActionFeedback.actual_temperature.isnot(None),
        )
        .order_by(ActionFeedback.created_at.asc())
        .all()
    )

    if not records:
        return {
            "comparison_type": "simulation_vs_actual",
            "records_compared": 0,
            "average_error": 0.0,
            "average_percentage_error": 0.0,
            "accurate_predictions": 0,
            "acceptable_predictions": 0,
            "inaccurate_predictions": 0,
            "accuracy_rate": 0.0,
            "comparisons": [],
            "interpretation": (
                "No simulation and actual-result records "
                "are available for comparison."
            ),
        }

    comparisons = []

    accurate_predictions = 0
    acceptable_predictions = 0
    inaccurate_predictions = 0

    absolute_errors = []
    percentage_errors = []

    for record in records:
        predicted = float(
            record.predicted_temperature
        )

        actual = float(
            record.actual_temperature
        )

        absolute_error = abs(
            predicted - actual
        )

        if actual != 0:
            percentage_error = (
                absolute_error / abs(actual)
            ) * 100
        else:
            percentage_error = 0.0

        if absolute_error <= 2:
            prediction_status = "accurate"
            accurate_predictions += 1

        elif absolute_error <= 5:
            prediction_status = "acceptable"
            acceptable_predictions += 1

        else:
            prediction_status = "inaccurate"
            inaccurate_predictions += 1

        absolute_errors.append(
            absolute_error
        )

        percentage_errors.append(
            percentage_error
        )

        comparisons.append(
            {
                "feedback_id": record.id,
                "digital_twin_id": record.digital_twin_id,
                "action": record.action,
                "predicted_temperature": round(
                    predicted,
                    2,
                ),
                "actual_temperature": round(
                    actual,
                    2,
                ),
                "absolute_error": round(
                    absolute_error,
                    2,
                ),
                "percentage_error": round(
                    percentage_error,
                    2,
                ),
                "status": prediction_status,
                "outcome": record.outcome,
                "created_at": record.created_at,
            }
        )

    total_records = len(records)

    average_error = (
        sum(absolute_errors)
        / total_records
    )

    average_percentage_error = (
        sum(percentage_errors)
        / total_records
    )

    accuracy_rate = (
        accurate_predictions
        / total_records
    ) * 100

    if accuracy_rate >= 80:
        interpretation = (
            "Simulation predictions are highly consistent "
            "with actual outcomes."
        )
    elif accuracy_rate >= 60:
        interpretation = (
            "Simulation predictions show acceptable "
            "agreement with actual outcomes."
        )
    else:
        interpretation = (
            "Simulation predictions require improvement "
            "to better match actual outcomes."
        )

    return {
        "comparison_type": "simulation_vs_actual",
        "records_compared": total_records,
        "average_error": round(
            average_error,
            2,
        ),
        "average_percentage_error": round(
            average_percentage_error,
            2,
        ),
        "accurate_predictions": accurate_predictions,
        "acceptable_predictions": acceptable_predictions,
        "inaccurate_predictions": inaccurate_predictions,
        "accuracy_rate": round(
            accuracy_rate,
            2,
        ),
        "comparisons": comparisons,
        "interpretation": interpretation,
    }