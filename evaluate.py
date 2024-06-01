import numpy as np

from core.evaluator import RSIEvaluator
from config import init_logging

init_logging()

evaluator = RSIEvaluator(
    broker="XTB",
    symbol="SOP.FR_9",
    period="1"
)

# stop_loss_values = np.arange(0.01, 0.11, 0.01)
# take_profit_values = np.arange(0.05, 0.51, 0.05)
# rsi_window_values = np.arange(10, 21, 1)
# overbought_threshold_values = np.arange(55, 90, 5)
# oversold_threshold_values = np.arange(10, 45, 5)
# Result: ????

stop_loss_values = np.arange(0.01, 0.03, 0.01)
take_profit_values = np.arange(0.05, 0.1, 0.05)
rsi_window_values = np.arange(10, 11, 1)
overbought_threshold_values = np.arange(55, 60, 5)
oversold_threshold_values = np.arange(10, 15, 5)

params = {
    'stop_loss_values': stop_loss_values,
    'take_profit_values': take_profit_values,
    'rsi_window_values': rsi_window_values,
    'overbought_threshold_values': overbought_threshold_values,
    'oversold_threshold_values': oversold_threshold_values
}

evaluator.grid_search(params, 2)
evaluator.save_results("./data/results/tmp.csv")

# rsi = RSIBasedStrategy(data=SopraReader.getDataframe(), backtest_strategy_class=BacktestRSI, stop_loss=0.05,
#                       take_profit=0.40)

# print(rs.run_backtest())
# rsi.plot_data_with_signals()
# rsi.plot_backtest_with_signals()

# alpha_api = AlphaVantageAPI(ALPHA_VANTAGE_API_KEY)
# alpha_api.get_daily_data("IBM")
