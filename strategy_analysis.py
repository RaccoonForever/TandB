from core.backtest import BacktestRSI, BacktestLong
from config import init_logging
from core.indicators.FVGIndicator import FVGIndicator
from core.trading import RSIBasedStrategy, FVGBasedStrategy
from core.utils.CsvReader import CsvReader

init_logging()

reader = CsvReader("data/XTB/SOP.FR_9_60.csv")

# rsi = RSIBasedStrategy(data=reader.get_dataframe().head(150), backtest_strategy_class=BacktestRSI, stop_loss=0.05,
#                       take_profit=0.40)

# print(rsi.run_backtest())
# rsi.plot_data_with_signals_v2()
# rsi.plot_backtest_with_signals()

fvg = FVGBasedStrategy(data=reader.get_dataframe().head(154), backtest_strategy_class=BacktestLong,
                       merge_consecutive_fvg_start=False,
                       merge_consecutive_fvg_end=False,
                       min_number_consecutive=2,
                       stop_loss=0.02,
                       take_profit=0.02,
                       retention_period=15,
                       FVG_min_size=0.1
                       )
# fvg.run_backtest()
print(fvg.generate_signals())

fvg.plot_data_with_signals_v2()
