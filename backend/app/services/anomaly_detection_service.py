from typing import Any


THRESHOLDS = {
    "temperature": 90.0,
    "vibration": 5.0,
    "power_usage": 25.0,
    "operating_speed": 1800.0,
}


def detect_anomalies(sensor_data: dict[str, Any]) -> dict[str, Any]:
    """
    Detect abnormal sensor readings using predefined
    operational thresholds.
    """

    anomalies = []

    temperature = float(sensor_data["temperature"])
    vibration = float(sensor_data["vibration"])
    power_usage = float(sensor_data["power_usage"])
    operating_speed = float(sensor_data["operating_speed"])

    if temperature > THRESHOLDS["temperature"]:
        anomalies.append(
            {
                "sensor": "temperature",
                "value": temperature,
                "threshold": THRESHOLDS["temperature"],
                "message": "Temperature exceeds safe threshold.",
            }
        )

    if vibration > THRESHOLDS["vibration"]:
        anomalies.append(
            {
                "sensor": "vibration",
                "value": vibration,
                "threshold": THRESHOLDS["vibration"],
                "message": "Vibration exceeds safe threshold.",
            }
        )

    if power_usage > THRESHOLDS["power_usage"]:
        anomalies.append(
            {
                "sensor": "power_usage",
                "value": power_usage,
                "threshold": THRESHOLDS["power_usage"],
                "message": "Power usage exceeds safe threshold.",
            }
        )

    if operating_speed > THRESHOLDS["operating_speed"]:
        anomalies.append(
            {
                "sensor": "operating_speed",
                "value": operating_speed,
                "threshold": THRESHOLDS["operating_speed"],
                "message": "Operating speed exceeds safe threshold.",
            }
        )

    return {
        "is_anomaly": len(anomalies) > 0,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
    }