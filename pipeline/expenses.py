from typing import Dict


def calculate_monthly_expenses(expenses: Dict[str, float]) -> float:
    """
    Calculate the total monthly expenses.

    Args:
        expenses: A dictionary containing various expense categories and their amounts.

    Returns:
        Total monthly expenses in JPY.
    """
    try:
        total = sum(expenses.values())
        if total < 0:
            raise ValueError("Total expenses cannot be negative.")
        return total
    except TypeError:
        raise ValueError("All expense parameters must be numerical.")
