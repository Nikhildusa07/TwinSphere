import numpy as np


def generate_training_data(samples: int = 1000):
    """
    Generate realistic historical sensor data for
    training the TwinSphere prediction model.

    The target represents the next expected temperature.
    """

    rng = np.random.default_rng(42)

    temperature = rng.normal(75, 8, samples)
    vibration = rng.normal(3.0, 0.8, samples)
    power_usage = rng.normal(17, 3, samples)
    operating_speed = rng.normal(1450, 120, samples)

    temperature = np.clip(temperature, 50, 100)
    vibration = np.clip(vibration, 0.5, 6)
    power_usage = np.clip(power_usage, 8, 30)
    operating_speed = np.clip(operating_speed, 900, 1800)

    next_temperature = (
        temperature
        + (vibration * 1.2)
        + (power_usage * 0.15)
        + ((operating_speed - 1400) * 0.01)
        + rng.normal(0, 1.5, samples)
    )

    X = np.column_stack(
        [
            temperature,
            vibration,
            power_usage,
            operating_speed,
        ]
    )

    y = next_temperature

    return X, y