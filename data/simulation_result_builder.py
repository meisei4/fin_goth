import json
from typing import List, Dict


class SimulationResult:
    def __init__(self, monthly_logs: List[Dict]):
        self.monthly_logs = monthly_logs

    def to_json(self) -> str:
        return json.dumps(self.monthly_logs, indent=4)

    def print_summary(self):
        summary = []
        base_indent = "  "
        for log_index, log in enumerate(self.monthly_logs):
            summary.append(f"「MONTH {log['month']} DETAILS」")

            asset_count = len(log['updated_portfolio'])
            for index, (asset, details) in enumerate(log['updated_portfolio'].items()):
                initial_value = log['initial_values'][asset]
                final_value = details['value']
                monthly_change = log['percentage_changes'].get(asset, 0)
                realized_pl = log['withdrawal_details'].get(asset, 0)
                all_time_change = log['total_percentage_changes'].get(asset, 0)

                is_last_asset = index == asset_count - 1
                connector = "└─" if is_last_asset else "├─"
                sub_connector = "  " if is_last_asset else "│ "

                asset_info = (
                    f"{base_indent}{connector} {asset}:\n"
                    f"{base_indent}{sub_connector}  ├─ Initial: {initial_value:,.0f} USD | "
                    f"Final: {final_value:,.0f} USD | Realized P/L: {realized_pl:,.0f} USD\n"
                    f"{base_indent}{sub_connector}  └─ Monthly Change: {monthly_change:+.2f}% | "
                    f"All-Time Change: {all_time_change:+.2f}%"
                )
                summary.append(asset_info)

            summary.append(f"「MONTH {log['month']} SUMMARY」")
            summary.append(
                f"{base_indent}├───── Expenses: {log['expenses_jpy']:,.0f} JPY ({log['expenses_usd']:,.0f} USD)\n"
                f"{base_indent}│\n"  # Extends the vertical line
                f"{base_indent}├───── Total Withdrawn: {log['total_withdrawn_usd']:,.0f} USD\n"
                f"{base_indent}│\n"  # Extends the vertical line
                f"{base_indent}├───── Cumulative Realized P/L: {log['cumulative_realized_pl']:,.0f} USD\n"
                f"{base_indent}│\n"  # Extends the vertical line
                f"{base_indent}├───── FX Rate: {log['current_fx_rate']:,.2f} JPY/USD\n"
                f"{base_indent}│\n"  # Extends the vertical line
                f"{base_indent}└───── Total Portfolio Value: {log['portfolio_value_usd']:,.0f} USD"
            )

            if log_index != len(self.monthly_logs) - 1:
                summary.append("")  # Blank line for separation between months
        print("\n".join(summary))

    def export_to_file(self, file_path: str):
        with open(file_path, 'w') as f:
            f.write(self.to_json())


class SimulationResultBuilder:
    def __init__(self):
        self.current_log = {}
        self.monthly_logs = []
        self.initial_values_set = False  # Track if initial_values has been set

    def add_month(self, month: int) -> 'SimulationResultBuilder':
        self.current_log['month'] = month
        return self

    def add_initial_values(self, initial_values: Dict[str, float]) -> 'SimulationResultBuilder':
        if not self.initial_values_set:
            self.initial_values = initial_values
            self.initial_values_set = True
        return self

    def add_expenses(self, expenses_jpy: float, expenses_usd: float) -> 'SimulationResultBuilder':
        self.current_log['expenses_jpy'] = expenses_jpy
        self.current_log['expenses_usd'] = expenses_usd
        return self

    def add_withdrawal(self, withdrawal_amount_usd: float, total_withdrawn_usd: float) -> 'SimulationResultBuilder':
        self.current_log['withdrawal_amount_usd'] = withdrawal_amount_usd
        self.current_log['total_withdrawn_usd'] = total_withdrawn_usd
        return self

    def add_realized_pl(self, realized_pl: float, cumulative_realized_pl: float) -> 'SimulationResultBuilder':
        self.current_log['realized_pl'] = realized_pl
        self.current_log['cumulative_realized_pl'] = cumulative_realized_pl
        return self

    def add_fx_rate(self, current_fx_rate: float) -> 'SimulationResultBuilder':
        self.current_log['current_fx_rate'] = current_fx_rate
        return self

    def add_portfolio(self, portfolio_value_usd: float, updated_portfolio: Dict[str, Dict[str, float]]) -> 'SimulationResultBuilder':
        self.current_log['portfolio_value_usd'] = portfolio_value_usd
        self.current_log['updated_portfolio'] = {k: v.copy() for k, v in updated_portfolio.items()}
        return self

    def add_changes(self, percentage_changes: Dict[str, float], total_percentage_changes: Dict[str, float]) -> 'SimulationResultBuilder':
        self.current_log['percentage_changes'] = percentage_changes
        self.current_log['total_percentage_changes'] = total_percentage_changes
        return self

    def add_withdrawal_details(self, withdrawal_details: Dict[str, float]) -> 'SimulationResultBuilder':
        self.current_log['withdrawal_details'] = withdrawal_details
        return self

    def complete_month(self) -> 'SimulationResultBuilder':
        # Ensure all necessary fields are set
        self.current_log.setdefault('withdrawal_details', {})
        self.current_log.setdefault('initial_values', self.initial_values)  # Set initial_values for this month
        self.monthly_logs.append(self.current_log)
        self.current_log = {}
        return self

    def build(self) -> SimulationResult:
        return SimulationResult(self.monthly_logs)
