from app.services.resource_allocation_service import allocate_resources


def main():
    test_cases = [
        {
            "risk_level": "low",
            "current_load": 100,
        },
        {
            "risk_level": "medium",
            "current_load": 100,
        },
        {
            "risk_level": "high",
            "current_load": 100,
        },
        {
            "risk_level": "critical",
            "current_load": 100,
        },
    ]

    for test_case in test_cases:
        result = allocate_resources(
            risk_level=test_case["risk_level"],
            current_load=test_case["current_load"],
        )

        print(f"\nRisk level: {test_case['risk_level']}")
        print(result)


if __name__ == "__main__":
    main()