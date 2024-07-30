from typing import Dict, Tuple

def calculate_monthly_withdrawal_amount(monthly_expenses_usd: float) -> float:
    """
    Calculate the monthly withdrawal amount.

    Args:
        monthly_expenses_usd: Monthly expenses in USD.

    Returns:
        Withdrawal amount in USD.
    """
    if monthly_expenses_usd < 0:
        raise ValueError("Monthly expenses cannot be negative.")
    return monthly_expenses_usd

def update_portfolio(
        portfolio: Dict[str, Dict[str, float]],
        withdrawal_amount_usd: float
) -> Tuple[Dict[str, Dict[str, float]], Dict[str, float], float]:
    """
    Update the portfolio after a withdrawal.

    Args:
        portfolio: A dictionary containing portfolio assets and their details.
        withdrawal_amount_usd: Amount to withdraw in USD.

    Returns:
        Updated portfolio, withdrawal details, and realized P/L.
    """
    total_portfolio_value = sum(asset['value'] for asset in portfolio.values())
    if total_portfolio_value <= 0:
        raise ValueError("Total portfolio value must be positive.")

    withdrawal_details = {}
    total_realized_pl = 0

    for asset_name, asset_data in portfolio.items():
        asset_value = asset_data['value']
        asset_cost_basis = asset_data['cost_basis']

        proportion = asset_value / total_portfolio_value
        withdrawal_amount_for_asset = withdrawal_amount_usd * proportion

        # Separate the effects of market price changes from withdrawals.
        unrealized_pl_since_start = asset_value - asset_cost_basis
        realized_pl_for_asset = withdrawal_amount_for_asset if unrealized_pl_since_start >= 0 else -withdrawal_amount_for_asset

        total_realized_pl += realized_pl_for_asset
        asset_data['value'] -= withdrawal_amount_for_asset
        withdrawal_details[asset_name] = withdrawal_amount_for_asset

    return portfolio, withdrawal_details, total_realized_pl
