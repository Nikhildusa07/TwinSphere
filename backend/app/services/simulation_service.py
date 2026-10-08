from typing import Any


def simulate_future_state(
    sensor_data: dict[str, Any],
    temperature_change: float = 0.0,
    vibration_change: float = 0.0,
    power_usage_change: float = 0.0,
    operating_speed_change: float = 0.0,
) -> dict[str, Any]:
    """
    Simulate a future digital-twin state by applying
    user-defined changes to the current sensor state.
    """

    current_state = {
        "temperature": float(sensor_data["temperature"]),
        "vibration": float(sensor_data["vibration"]),
        "power_usage": float(sensor_data["power_usage"]),
        "operating_speed": float(sensor_data["operating_speed"]),
    }

    simulated_state = {
        "temperature": current_state["temperature"] + temperature_change,
        "vibration": current_state["vibration"] + vibration_change,
        "power_usage": current_state["power_usage"] + power_usage_change,
        "operating_speed": (
            current_state["operating_speed"]
            + operating_speed_change
        ),
    }

    return {
        "current_state": current_state,
        "simulated_state": simulated_state,
        "changes": {
            "temperature": temperature_change,
            "vibration": vibration_change,
            "power_usage": power_usage_change,
            "operating_speed": operating_speed_change,
        },
    }