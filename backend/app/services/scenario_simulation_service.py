from typing import Any

from app.services.risk_analysis_service import calculate_risk_level
from app.services.simulation_service import simulate_future_state


def simulate_scenarios(
    sensor_data: dict[str, Any],
    scenarios: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Simulate multiple future scenarios and calculate
    the risk level for each simulated state.
    """

    results = []

    for scenario in scenarios:
        simulation = simulate_future_state(
            sensor_data=sensor_data,
            temperature_change=float(
                scenario.get("temperature_change", 0.0)
            ),
            vibration_change=float(
                scenario.get("vibration_change", 0.0)
            ),
            power_usage_change=float(
                scenario.get("power_usage_change", 0.0)
            ),
            operating_speed_change=float(
                scenario.get("operating_speed_change", 0.0)
            ),
        )

        risk = calculate_risk_level(
            simulation["simulated_state"]
        )

        results.append(
            {
                "scenario": scenario.get(
                    "name",
                    f"Scenario {len(results) + 1}",
                ),
                "simulated_state": simulation["simulated_state"],
                "risk_score": risk["risk_score"],
                "risk_level": risk["risk_level"],
                "risk_factors": risk["risk_factors"],
            }
        )

    return results