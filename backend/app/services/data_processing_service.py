from typing import Any

import pandas as pd


def process_sensor_data(sensor_data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate and preprocess incoming sensor data.

    Converts sensor values to numeric values and checks
    for missing or invalid readings.
    """

    required_fields = [
        "temperature",
        "vibration",
        "power_usage",
        "operating_speed",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in sensor_data
    ]

    if missing_fields:
        raise ValueError(
            f"Missing sensor fields: {', '.join(missing_fields)}"
        )

    dataframe = pd.DataFrame([sensor_data])

    for field in required_fields:
        dataframe[field] = pd.to_numeric(
            dataframe[field],
            errors="coerce",
        )

    if dataframe[required_fields].isnull().any().any():
        raise ValueError(
            "Sensor data contains invalid numeric values."
        )

    processed_data = dataframe.iloc[0].to_dict()

    processed_data["temperature"] = float(
        processed_data["temperature"]
    )
    processed_data["vibration"] = float(
        processed_data["vibration"]
    )
    processed_data["power_usage"] = float(
        processed_data["power_usage"]
    )
    processed_data["operating_speed"] = float(
        processed_data["operating_speed"]
    )

    return processed_data