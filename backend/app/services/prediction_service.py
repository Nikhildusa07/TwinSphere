from typing import Any

import numpy as np

from app.ml.prediction_model import create_prediction_model


FEATURES = [
    "temperature",
    "vibration",
    "power_usage",
    "operating_speed",
]


def prepare_prediction_features(
    sensor_data: dict[str, Any],
) -> np.ndarray:
    """
    Convert processed sensor data into an ML-ready feature array.
    """

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in sensor_data
    ]

    if missing_features:
        raise ValueError(
            f"Missing prediction features: {', '.join(missing_features)}"
        )

    features = np.array(
        [
            [
                float(sensor_data["temperature"]),
                float(sensor_data["vibration"]),
                float(sensor_data["power_usage"]),
                float(sensor_data["operating_speed"]),
            ]
        ],
        dtype=float,
    )

    return features


def create_prediction_engine():
    """
    Create the prediction model used by TwinSphere.
    """

    return create_prediction_model()