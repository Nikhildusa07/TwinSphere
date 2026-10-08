from typing import Any


def recommend_action(
    scenario_results: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Select the safest scenario and recommend an action
    based on the lowest predicted risk.
    """

    if not scenario_results:
        raise ValueError("No scenario results provided.")

    safest_scenario = min(
        scenario_results,
        key=lambda scenario: scenario["risk_score"],
    )

    risk_level = safest_scenario["risk_level"]

    if risk_level == "critical":
        action = "Stop operation and inspect the system immediately."
    elif risk_level == "high":
        action = "Reduce operating load and perform preventive inspection."
    elif risk_level == "medium":
        action = "Monitor the system closely and adjust operating conditions."
    else:
        action = "Continue normal operation."

    return {
        "recommended_scenario": safest_scenario["scenario"],
        "risk_score": safest_scenario["risk_score"],
        "risk_level": risk_level,
        "action": action,
        "reason": (
            "Selected the scenario with the lowest predicted "
            "operational risk."
        ),
    }   