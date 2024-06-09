import numpy as np

from core.evaluator import FVGEvaluator
from config import init_logging

init_logging()

evaluator = FVGEvaluator(
    broker="XTB",
    symbol="SOP.FR_9",
    period="60",

)

stop_loss_values = np.arange(0.01, 0.05, 0.01)
take_profit_values = np.arange(0.01, 0.5, 0.02)
retention_period_values = np.arange(16, 26, 2)
FVG_min_size_values = np.arange(0.04, 0.1, 0.02)
merge_consecutive_fvg_start_values = [False]
breaking_support_trigger_values = ["Top", "Bottom"]

params = {
    'stop_loss_values': stop_loss_values,
    'take_profit_values': take_profit_values,
    'retention_period_values': retention_period_values,
    'FVG_min_size_values': FVG_min_size_values,
    'merge_consecutive_fvg_start_values': merge_consecutive_fvg_start_values,
    'breaking_support_trigger_values': breaking_support_trigger_values
}

evaluator.grid_search(params, 10)
evaluator.save_results()
evaluator.print_results()

# rsi = RSIBasedStrategy(data=SopraReader.getDataframe(), backtest_strategy_class=BacktestRSI, stop_loss=0.05,
#                       take_profit=0.40)

# print(rs.run_backtest())
# rsi.plot_data_with_signals()
# rsi.plot_backtest_with_signals()

# alpha_api = AlphaVantageAPI(ALPHA_VANTAGE_API_KEY)
# alpha_api.get_daily_data("IBM")
