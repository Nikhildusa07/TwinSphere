from typing import Any


def allocate_resources(
    risk_level: str,
    current_load: float,
) -> dict[str, Any]:
    """
    Recommend operational resource allocation based on
    the current risk level and system load.
    """

    if current_load < 0:
        raise ValueError("Current load cannot be negative.")

    if risk_level == "critical":
        allocation = {
            "load_reduction_percent": 40,
            "maintenance_priority": "immediate",
            "monitoring_level": "continuous",
            "resource_action": "Allocate maximum maintenance resources.",
        }

    elif risk_level == "high":
        allocation = {
            "load_reduction_percent": 25,
            "maintenance_priority": "high",
            "monitoring_level": "frequent",
            "resource_action": "Increase maintenance and monitoring resources.",
        }

    elif risk_level == "medium":
        allocation = {
            "load_reduction_percent": 10,
            "maintenance_priority": "normal",
            "monitoring_level": "regular",
            "resource_action": "Maintain normal resources with closer monitoring.",
        }

    else:
        allocation = {
            "load_reduction_percent": 0,
            "maintenance_priority": "low",
            "monitoring_level": "normal",
            "resource_action": "Continue normal resource allocation.",
        }

    adjusted_load = current_load * (
        1 - allocation["load_reduction_percent"] / 100
    )

    return {
        "current_load": current_load,
        "adjusted_load": round(adjusted_load, 2),
        "risk_level": risk_level,
        **allocation,
    }