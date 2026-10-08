from app.services.action_planning_service import create_action_plan


def main():
    resource_allocation = {
        "current_load": 100,
        "adjusted_load": 75,
        "risk_level": "high",
        "load_reduction_percent": 25,
        "maintenance_priority": "high",
        "monitoring_level": "frequent",
        "resource_action": (
            "Increase maintenance and monitoring resources."
        ),
    }

    result = create_action_plan(
        risk_level="high",
        recommended_action=(
            "Reduce operating load and perform preventive inspection."
        ),
        resource_allocation=resource_allocation,
    )

    print("Autonomous action plan:")
    print(result)


if __name__ == "__main__":
    main()