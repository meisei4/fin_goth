# main.py

from config import Config
from pipeline.assets import simulate_asset_values, simulate_fx_rate
from pipeline.expenses import calculate_monthly_expenses
from pipeline.logger import logger
from pipeline.portfolio import calculate_monthly_withdrawal_amount, update_portfolio
from data.simulation_result_builder import SimulationResultBuilder


def simulate_expenses_withdrawn_over_monthly_asset_volatility(portfolio, months, expenses_params):
    result_builder = SimulationResultBuilder()
    initial_values = {asset: details['value'] for asset, details in portfolio.items()}
    result_builder.add_initial_values(initial_values)

    current_fx_rate = Config.STARTING_FX_RATE
    total_withdrawn = 0
    cumulative_realized_pl = 0

    for month in range(1, months + 1):
        logger.info(f"Simulating month {month}")

        percentage_changes = simulate_asset_values(portfolio)
        total_percentage_changes = {
            asset: ((portfolio[asset]['value'] - initial_values[asset]) / initial_values[asset]) * 100
            for asset in portfolio
        }
        current_fx_rate = simulate_fx_rate(current_fx_rate)

        monthly_expenses_jpy = calculate_monthly_expenses(expenses_params)
        monthly_expenses_usd = monthly_expenses_jpy / current_fx_rate

        monthly_withdrawal_amount_usd = calculate_monthly_withdrawal_amount(monthly_expenses_usd)
        updated_portfolio, withdrawal_details, realized_pl = update_portfolio(portfolio, monthly_withdrawal_amount_usd)

        total_withdrawn += monthly_withdrawal_amount_usd
        cumulative_realized_pl += realized_pl

        logger.debug(f"Month {month} Summary: "
                     f"Expenses JPY: {monthly_expenses_jpy}, "
                     f"Expenses USD: {monthly_expenses_usd}, "
                     f"Withdrawal USD: {monthly_withdrawal_amount_usd}, "
                     f"Realized P/L: {realized_pl}, "
                     f"Total Withdrawn USD: {total_withdrawn}, "
                     f"Cumulative Realized P/L: {cumulative_realized_pl}")

        result_builder.add_month(month) \
            .add_expenses(monthly_expenses_jpy, monthly_expenses_usd) \
            .add_withdrawal(monthly_withdrawal_amount_usd, total_withdrawn) \
            .add_realized_pl(realized_pl, cumulative_realized_pl) \
            .add_fx_rate(current_fx_rate) \
            .add_portfolio(sum(asset['value'] for asset in portfolio.values()), updated_portfolio) \
            .add_changes(percentage_changes, total_percentage_changes) \
            .add_withdrawal_details(withdrawal_details) \
            .complete_month()

    return result_builder.build()


def main():
    portfolio = Config.portfolio_assets.copy()
    expenses_params = Config.get_expenses_params()
    simulation_result = simulate_expenses_withdrawn_over_monthly_asset_volatility(portfolio, Config.MONTHS, expenses_params)

    # Print the result summary to the console
    simulation_result.print_summary()

    # Optionally export to a file (for future needs)
    # simulation_result.export_to_file('simulation_summary.txt')
    # simulation_result.export_to_file('simulation_results.json')


if __name__ == "__main__":
    main()
