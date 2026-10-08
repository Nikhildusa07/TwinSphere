from app.services.simulation_service import simulate_future_state


def main():
    sensor_data = {
        "temperature": 82.3,
        "vibration": 3.9,
        "power_usage": 18.7,
        "operating_speed": 1520,
    }

    result = simulate_future_state(
        sensor_data=sensor_data,
        temperature_change=5.0,
        vibration_change=0.5,
        power_usage_change=2.0,
        operating_speed_change=100.0,
    )

    print("Simulation result:")
    print(result)


if __name__ == "__main__":
    main()