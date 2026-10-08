from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.action_feedback import ActionFeedback
from app.schemas.action_feedback import (
    ActionFeedbackCreate,
    ActionFeedbackResponse,
)
from app.services.action_feedback_service import create_action_feedback
from app.services.continuous_learning_service import evaluate_learning_need
from app.services.feedback_analysis_service import analyze_prediction_accuracy


router = APIRouter(
    prefix="/feedback",
    tags=["Action Feedback"],
)


@router.post(
    "/",
    response_model=ActionFeedbackResponse,
)
def submit_action_feedback(
    feedback: ActionFeedbackCreate,
    db: Session = Depends(get_db),
):
    """
    Store the outcome of an autonomous action and
    compare predicted and actual temperature.
    """

    try:
        return create_action_feedback(
            db=db,
            feedback_data=feedback.model_dump(),
        )

    except (TypeError, ValueError, KeyError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.get(
    "/",
    response_model=list[ActionFeedbackResponse],
)
def get_action_feedback(
    db: Session = Depends(get_db),
):
    """
    Return all stored action feedback records.
    """

    return (
        db.query(ActionFeedback)
        .order_by(ActionFeedback.created_at.desc())
        .all()
    )


@router.get(
    "/accuracy",
)
def get_prediction_accuracy(
    db: Session = Depends(get_db),
):
    """
    Analyze prediction accuracy using stored
    feedback records.
    """

    return analyze_prediction_accuracy(db)


@router.get(
    "/learning-status",
)
def get_learning_status(
    db: Session = Depends(get_db),
    retraining_threshold: float = 5.0,
):
    """
    Evaluate prediction performance and determine
    whether model retraining is recommended.
    """

    try:
        return evaluate_learning_need(
            db=db,
            retraining_threshold=retraining_threshold,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error