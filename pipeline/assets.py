from typing import Dict, Any

import numpy as np


def simulate_asset_values(portfolio: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
    """
    Simulate the monthly asset value changes.

    Args:
        portfolio: A dictionary containing portfolio assets and their details.

    Returns:
        A dictionary with asset names as keys and their percentage changes as values.
    """
    percentage_changes = {}
    for asset, details in portfolio.items():
        previous_value = details.get('value', 0)
        asset_return = details.get('return', 0)
        volatility = details.get('volatility', 0)

        if previous_value <= 0:
            percentage_changes[asset] = 0
            continue

        monthly_return = np.random.normal(asset_return / 12, volatility / np.sqrt(12))
        new_value = max(previous_value * (1 + monthly_return), 0)  # Prevent negative value
        details['value'] = new_value

        percentage_change = ((new_value - previous_value) / previous_value) * 100
        percentage_changes[asset] = percentage_change

        # TODO: Ensure percentage changes only reflect market price changes, not withdrawals.

    return percentage_changes


def simulate_fx_rate(current_rate: float, avg_change: float = 0.0, volatility: float = 0.01) -> float:
    """
    Simulate the fluctuation of the FX rate.

    Args:
        current_rate: Current FX rate.
        avg_change: Average change in FX rate (default is 0.0).
        volatility: Volatility of the FX rate (default is 0.01).

    Returns:
        New FX rate.
    """
    if current_rate <= 0:
        raise ValueError("Current FX rate must be positive.")

    monthly_fluctuation = np.random.normal(avg_change, volatility)
    new_rate = max(current_rate * (1 + monthly_fluctuation), 0.01)  # Prevent rate from going below a minimum threshold
    return new_rate
