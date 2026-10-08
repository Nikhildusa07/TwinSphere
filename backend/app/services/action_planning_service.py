from typing import Any


def create_action_plan(
    risk_level: str,
    recommended_action: str,
    resource_allocation: dict[str, Any],
) -> dict[str, Any]:
    """
    Create an autonomous operational action plan
    using risk level, recommended action, and
    resource allocation information.
    """

    if not recommended_action:
        raise ValueError("Recommended action is required.")

    normalized_risk_level = str(risk_level).strip().lower()

    if normalized_risk_level == "critical":
        priority = "critical"
        actions = [
            "Stop or isolate the affected operation.",
            "Inspect the system immediately.",
            "Allocate maximum maintenance resources.",
            "Continuously monitor sensor conditions.",
        ]

    elif normalized_risk_level == "high":
        priority = "high"
        actions = [
            "Reduce operating load.",
            "Schedule preventive inspection.",
            "Increase sensor monitoring frequency.",
            "Prepare maintenance resources.",
        ]

    elif normalized_risk_level == "medium":
        priority = "medium"
        actions = [
            "Adjust operating conditions.",
            "Monitor sensor conditions regularly.",
            "Review system performance.",
        ]

    else:
        priority = "low"
        actions = [
            "Continue normal operation.",
            "Maintain standard monitoring.",
        ]

    return {
        "priority": priority,
        "recommended_action": recommended_action,
        "actions": actions,
        "resource_allocation": resource_allocation,
    }