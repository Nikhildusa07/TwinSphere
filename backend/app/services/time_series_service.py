from typing import Any

import numpy as np
from sklearn.linear_model import LinearRegression


def analyze_time_series(
    sensor_records: list[dict[str, Any]],
    moving_average_window: int = 3,
) -> dict[str, Any]:
    """
    Perform time-series analysis on historical temperature data.

    The analysis includes:
    - historical temperature readings
    - moving average
    - linear trend
    - trend direction
    - next-step temperature forecast
    """

    if len(sensor_records) < 3:
        raise ValueError(
            "At least 3 historical sensor records are required "
            "for time-series analysis."
        )

    if moving_average_window <= 0:
        raise ValueError(
            "Moving average window must be greater than zero."
        )

    temperatures = []

    for record in sensor_records:
        try:
            temperatures.append(
                float(record["temperature"])
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                "Historical sensor records contain invalid "
                "temperature values."
            ) from error

    if moving_average_window > len(temperatures):
        moving_average_window = len(temperatures)

    values = np.array(
        temperatures,
        dtype=float,
    )

    time_index = np.arange(
        len(values),
        dtype=float,
    ).reshape(-1, 1)

    model = LinearRegression()
    model.fit(time_index, values)

    slope = float(model.coef_[0])
    forecast_index = np.array(
        [[float(len(values))]]
    )

    predicted_temperature = float(
        model.predict(forecast_index)[0]
    )

    moving_average_values = []

    for index in range(
        moving_average_window - 1,
        len(values),
    ):
        window = values[
            index - moving_average_window + 1:
            index + 1
        ]

        moving_average_values.append(
            round(float(np.mean(window)), 2)
        )

    recent_window = values[
        -moving_average_window:
    ]

    recent_average = float(
        np.mean(recent_window)
    )

    if slope > 0.5:
        trend_direction = "increasing"
    elif slope < -0.5:
        trend_direction = "decreasing"
    else:
        trend_direction = "stable"

    if trend_direction == "increasing":
        interpretation = (
            "Temperature shows an increasing trend. "
            "The system should be monitored for rising "
            "operational conditions."
        )
    elif trend_direction == "decreasing":
        interpretation = (
            "Temperature shows a decreasing trend. "
            "Current operating conditions are moving toward "
            "lower temperature levels."
        )
    else:
        interpretation = (
            "Temperature remains relatively stable with "
            "no significant short-term trend."
        )

    return {
        "analysis_type": "advanced_temperature_time_series",
        "records_analyzed": len(values),
        "moving_average_window": moving_average_window,
        "historical_temperatures": [
            round(float(value), 2)
            for value in values
        ],
        "moving_average": moving_average_values,
        "recent_average_temperature": round(
            recent_average,
            2,
        ),
        "trend_slope": round(
            slope,
            4,
        ),
        "trend_direction": trend_direction,
        "forecasted_next_temperature": round(
            predicted_temperature,
            2,
        ),
        "interpretation": interpretation,
    }