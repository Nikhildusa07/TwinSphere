from typing import Any

from sqlalchemy.orm import Session

from app.models.action_feedback import ActionFeedback


def create_action_feedback(
    db: Session,
    feedback_data: dict[str, Any],
) -> ActionFeedback:
    """
    Store the result of an autonomous action and compare
    predicted and actual temperature when both are available.
    """

    predicted_temperature = feedback_data.get(
        "predicted_temperature"
    )

    actual_temperature = feedback_data.get(
        "actual_temperature"
    )

    outcome = feedback_data["outcome"]

    if (
        predicted_temperature is not None
        and actual_temperature is not None
    ):
        prediction_error = abs(
            float(predicted_temperature)
            - float(actual_temperature)
        )

        if prediction_error <= 2:
            outcome = "accurate"
        elif prediction_error <= 5:
            outcome = "acceptable"
        else:
            outcome = "inaccurate"

    feedback = ActionFeedback(
        digital_twin_id=feedback_data["digital_twin_id"],
        action=feedback_data["action"],
        predicted_temperature=predicted_temperature,
        actual_temperature=actual_temperature,
        outcome=outcome,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback