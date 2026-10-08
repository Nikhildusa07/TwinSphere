from typing import Any

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


FEATURES = [
    "vibration",
    "power_usage",
    "operating_speed",
]

TARGET = "temperature"


def analyze_causal_influence(
    sensor_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze the influence of operational variables
    on temperature using historical sensor data.

    This is a practical causal-analysis prototype based
    on correlation and standardized regression influence.
    It is not a formal causal inference model.
    """

    if len(sensor_records) < 2:
        raise ValueError(
            "At least 2 historical sensor records are required "
            "for causal analysis."
        )

    cleaned_records = []

    for record in sensor_records:
        try:
            cleaned_records.append(
                {
                    "temperature": float(record["temperature"]),
                    "vibration": float(record["vibration"]),
                    "power_usage": float(record["power_usage"]),
                    "operating_speed": float(
                        record["operating_speed"]
                    ),
                }
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                "Historical sensor records contain invalid values."
            ) from error

    X = np.array(
        [
            [
                record["vibration"],
                record["power_usage"],
                record["operating_speed"],
            ]
            for record in cleaned_records
        ],
        dtype=float,
    )

    y = np.array(
        [
            record["temperature"]
            for record in cleaned_records
        ],
        dtype=float,
    )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    influences = []

    for index, feature in enumerate(FEATURES):
        feature_values = X[:, index]

        if np.std(feature_values) == 0 or np.std(y) == 0:
            correlation = 0.0
        else:
            correlation = float(
                np.corrcoef(feature_values, y)[0, 1]
            )

        coefficient = float(model.coef_[index])

        if abs(coefficient) >= 2:
            influence_level = "strong"
        elif abs(coefficient) >= 0.5:
            influence_level = "moderate"
        else:
            influence_level = "weak"

        if coefficient > 0:
            direction = "increases temperature"
        elif coefficient < 0:
            direction = "decreases temperature"
        else:
            direction = "minimal temperature influence"

        influences.append(
            {
                "factor": feature,
                "correlation_with_temperature": round(
                    correlation,
                    4,
                ),
                "standardized_influence": round(
                    coefficient,
                    4,
                ),
                "influence_level": influence_level,
                "direction": direction,
            }
        )

    influences.sort(
        key=lambda item: abs(
            item["standardized_influence"]
        ),
        reverse=True,
    )

    strongest_factor = influences[0]

    return {
        "analysis_type": "historical_sensor_influence_analysis",
        "records_analyzed": len(cleaned_records),
        "target": TARGET,
        "factors": influences,
        "strongest_influencing_factor": (
            strongest_factor["factor"]
        ),
        "interpretation": (
            f"{strongest_factor['factor']} shows the strongest "
            f"modeled influence on temperature and "
            f"{strongest_factor['direction']}."
        ),
    }