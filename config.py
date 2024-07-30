class Config:
    # Simulation Parameters
    STARTING_FX_RATE = 110  # Example initial JPY/USD exchange rate
    SAFE_WITHDRAWAL_RATE_MONTHLY = 0.004  # Example monthly safe withdrawal rate (0.4%)
    MONTHS = 12  # Duration of the simulation in months

    # Example Annual Expenses
    # Uncomment and set these values based on specific needs
    # ANNUAL_TRAVEL_BUDGET_JPY = 300000  # Annual budget for travel
    # EDUCATION_FEES_ANNUAL_JPY = 800000  # Annual education fees
    # PROPERTY_TAX_ANNUAL_JPY = 250000  # Annual property tax
    # LOAN_PAYMENT_1_ANNUAL_JPY = 150000  # Annual loan payment 1
    # LOAN_PAYMENT_2_ANNUAL_JPY = 200000  # Annual loan payment 2

    # Monthly Expense Parameters
    # Define monthly costs in JPY for different categories
    GROCERY_EXPENSES_MONTHLY_JPY = 50000  # Monthly grocery expenses
    RENT_MONTHLY_JPY = 80000  # Monthly rent payment
    VEHICLE_MAINTENANCE_MONTHLY_JPY = 15000  # Monthly vehicle maintenance costs
    HEALTHCARE_EXPENSES_MONTHLY_JPY = 30000  # Monthly healthcare expenses
    ENTERTAINMENT_BUDGET_MONTHLY_JPY = 20000  # Monthly budget for entertainment
    UTILITIES_EXPENSES_MONTHLY_JPY = 25000  # Monthly utilities (electricity, water, etc.)
    INTERNET_AND_PHONE_MONTHLY_JPY = 10000  # Monthly internet and phone bills

    # Portfolio Setup
    # Define your investment portfolio with dummy data. Include each asset's current value, initial cost basis,
    # expected monthly return, and volatility.
    portfolio_assets = {
        'ABC_STOCK': {'value': 1000, 'cost_basis': 2000, 'return': 0.02, 'volatility': 0.15},  # Example stock
        'XYZ_BOND': {'value': 50000, 'cost_basis': 50000, 'return': 0.01, 'volatility': 0.05},   # Example bond
        'THING': {'value': 7000, 'cost_basis': 20000, 'return': 0.01, 'volatility': 0.30},     # Example thing
        'REAL_ESTATE': {'value': 5000, 'cost_basis': 5000, 'return': 0.01, 'volatility': 0.02}, # Real estate
        'MUTUAL_FUND': {'value': 7500, 'cost_basis': 7000, 'return': 0.015, 'volatility': 0.10},  # Mutual fund
    }

    @classmethod
    def get_expenses_params(cls):
        """
        Returns a dictionary of the monthly expense parameters.
        Users should call this method to retrieve their customized expense settings.
        """
        return {
            'grocery_expenses': cls.GROCERY_EXPENSES_MONTHLY_JPY,
            'rent': cls.RENT_MONTHLY_JPY,
            'vehicle_maintenance': cls.VEHICLE_MAINTENANCE_MONTHLY_JPY,
            'healthcare_expenses': cls.HEALTHCARE_EXPENSES_MONTHLY_JPY,
            'entertainment_budget': cls.ENTERTAINMENT_BUDGET_MONTHLY_JPY,
            'utilities_expenses': cls.UTILITIES_EXPENSES_MONTHLY_JPY,
            'internet_and_phone': cls.INTERNET_AND_PHONE_MONTHLY_JPY,
        }
