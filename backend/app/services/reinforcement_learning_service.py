from typing import Any


ACTIONS = [
    "maintain_current_operation",
    "reduce_operating_load",
    "perform_preventive_inspection",
]


def calculate_state(
    temperature: float,
    vibration: float,
    power_usage: float,
    operating_speed: float,
) -> str:
    """
    Convert sensor values into a simple operational state.
    """

    if (
        temperature > 90
        or vibration > 5
        or power_usage > 25
        or operating_speed > 1800
    ):
        return "critical"

    if (
        temperature > 80
        or vibration > 4
        or power_usage > 20
        or operating_speed > 1650
    ):
        return "high_risk"

    return "normal"


def calculate_reward(
    temperature: float,
    vibration: float,
    power_usage: float,
    operating_speed: float,
    action: str,
) -> float:
    """
    Calculate a reward for an operational action.

    Higher reward means the selected action is more suitable
    for the current machine state.
    """

    state = calculate_state(
        temperature,
        vibration,
        power_usage,
        operating_speed,
    )

    if state == "normal":
        rewards = {
            "maintain_current_operation": 10,
            "reduce_operating_load": 4,
            "perform_preventive_inspection": 2,
        }

    elif state == "high_risk":
        rewards = {
            "maintain_current_operation": -5,
            "reduce_operating_load": 10,
            "perform_preventive_inspection": 8,
        }

    else:
        rewards = {
            "maintain_current_operation": -10,
            "reduce_operating_load": 8,
            "perform_preventive_inspection": 12,
        }

    return float(rewards.get(action, 0))


def select_best_action(
    temperature: float,
    vibration: float,
    power_usage: float,
    operating_speed: float,
) -> dict[str, Any]:
    """
    Select the action with the highest estimated reward.
    """

    state = calculate_state(
        temperature,
        vibration,
        power_usage,
        operating_speed,
    )

    action_rewards = {}

    for action in ACTIONS:
        action_rewards[action] = calculate_reward(
            temperature,
            vibration,
            power_usage,
            operating_speed,
            action,
        )

    best_action = max(
        action_rewards,
        key=action_rewards.get,
    )

    return {
        "state": state,
        "recommended_action": best_action,
        "estimated_reward": action_rewards[best_action],
        "action_rewards": action_rewards,
        "learning_method": "rule-based reinforcement learning",
        "interpretation": (
            f"The reinforcement learning component selected "
            f"'{best_action}' for the current {state} state."
        ),
    }