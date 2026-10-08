from app.services.scenario_simulation_service import simulate_scenarios


def main():
    sensor_data = {
        "temperature": 82.3,
        "vibration": 3.9,
        "power_usage": 18.7,
        "operating_speed": 1520,
    }

    scenarios = [
        {
            "name": "Normal Operation",
            "temperature_change": 0,
            "vibration_change": 0,
            "power_usage_change": 0,
            "operating_speed_change": 0,
        },
        {
            "name": "Increased Load",
            "temperature_change": 5,
            "vibration_change": 0.5,
            "power_usage_change": 2,
            "operating_speed_change": 100,
        },
        {
            "name": "High Stress",
            "temperature_change": 12,
            "vibration_change": 1.5,
            "power_usage_change": 8,
            "operating_speed_change": 300,
        },
    ]

    results = simulate_scenarios(
        sensor_data=sensor_data,
        scenarios=scenarios,
    )

    print("Scenario simulation results:")

    for result in results:
        print("\nScenario:", result["scenario"])
        print("Simulated state:", result["simulated_state"])
        print("Risk score:", result["risk_score"])
        print("Risk level:", result["risk_level"])
        print("Risk factors:", result["risk_factors"])


if __name__ == "__main__":
    main()