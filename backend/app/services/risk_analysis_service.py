from typing import Any


def calculate_risk_level(
    sensor_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate the operational risk level based on
    current sensor conditions.
    """

    risk_score = 0
    risk_factors = []

    temperature = float(sensor_data["temperature"])
    vibration = float(sensor_data["vibration"])
    power_usage = float(sensor_data["power_usage"])
    operating_speed = float(sensor_data["operating_speed"])

    if temperature > 90:
        risk_score += 30
        risk_factors.append("High temperature")

    elif temperature > 80:
        risk_score += 15
        risk_factors.append("Elevated temperature")

    if vibration > 5:
        risk_score += 30
        risk_factors.append("High vibration")

    elif vibration > 4:
        risk_score += 15
        risk_factors.append("Elevated vibration")

    if power_usage > 25:
        risk_score += 20
        risk_factors.append("High power usage")

    elif power_usage > 20:
        risk_score += 10
        risk_factors.append("Elevated power usage")

    if operating_speed > 1800:
        risk_score += 20
        risk_factors.append("High operating speed")

    elif operating_speed > 1650:
        risk_score += 10
        risk_factors.append("Elevated operating speed")

    if risk_score >= 60:
        risk_level = "critical"
    elif risk_score >= 30:
        risk_level = "high"
    elif risk_score >= 15:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }