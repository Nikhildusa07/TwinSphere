from app.services.decision_engine_service import recommend_action


def main():
    scenario_results = [
        {
            "scenario": "Normal Operation",
            "simulated_state": {
                "temperature": 82.3,
                "vibration": 3.9,
                "power_usage": 18.7,
                "operating_speed": 1520,
            },
            "risk_score": 15,
            "risk_level": "medium",
            "risk_factors": [
                "Elevated temperature"
            ],
        },
        {
            "scenario": "Increased Load",
            "simulated_state": {
                "temperature": 87.3,
                "vibration": 4.4,
                "power_usage": 20.7,
                "operating_speed": 1620,
            },
            "risk_score": 40,
            "risk_level": "high",
            "risk_factors": [
                "Elevated temperature",
                "Elevated vibration",
                "Elevated power usage",
            ],
        },
        {
            "scenario": "High Stress",
            "simulated_state": {
                "temperature": 94.3,
                "vibration": 5.4,
                "power_usage": 26.7,
                "operating_speed": 1820,
            },
            "risk_score": 100,
            "risk_level": "critical",
            "risk_factors": [
                "High temperature",
                "High vibration",
                "High power usage",
                "High operating speed",
            ],
        },
    ]

    result = recommend_action(scenario_results)

    print("Decision engine result:")
    print(result)


if __name__ == "__main__":
    main()