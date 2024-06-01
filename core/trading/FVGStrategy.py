import logging

import pandas as pd
import numpy as np

from core.trading.Strategy import TradingStrategy
from core.indicators.FVGIndicator import FVGIndicator

logger = logging.getLogger(__name__)


class FVGBasedStrategy(TradingStrategy):

    def __init__(self, data, backtest_strategy_class, merge_consecutive_fvg_start=False,
                 merge_consecutive_fvg_end=False,
                 retention_period=100,
                 FVG_min_size=0.1,
                 stop_loss=None, take_profit=None):
        """
        Initialize the trading strategy with historical market data and FVG parameters.

        Args:
        - data (DataFrame): Historical market data.
        - merge_consecutive_fvg_start (boolean): Do we merge multiple FVG to the first detected one.
        - merge_consecutive_fvg_end (boolean): Do we merge multiple FVG to the last detected one.
        - retention_period (int): How much time do we keep an FVG to allow a signal (buy).
        - FVG_min_size (float): The minimum size of the FVG to allow a signal (buy) in percent of the asset price.
        - stop_loss (float or None): Stop loss percentage (e.g., 0.05 for 5%) for exiting a losing trade.
        - take_profit (float or None): Take profit percentage (e.g., 0.1 for 10%) for exiting a winning trade.
        """
        super().__init__(data, backtest_strategy_class)
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.merge_consecutive_fvg_start = merge_consecutive_fvg_start
        self.merge_consecutive_fvg_end = merge_consecutive_fvg_end
        self.retention_period = retention_period
        self.FVG_min_size = FVG_min_size

    def generate_signals(self):
        """
        Generate buy/sell signals based on RSI.

        Returns:
        - signals (DataFrame): DataFrame containing buy/sell signals.
        """
        fvg_indicator = FVGIndicator(self.data,
                                     merge_consecutive_fvg_start=self.merge_consecutive_fvg_start,
                                     merge_consecutive_fvg_end=self.merge_consecutive_fvg_end)
        fvg_values = fvg_indicator.calculate()

        fvg_values_index_int = fvg_values.reset_index()
        data_index_int = self.data.reset_index()

        signals = pd.DataFrame()
        signals['date'] = self.data.index
        signals['FVG'] = fvg_values_index_int['FVG']
        signals['open'] = data_index_int.loc[:, 'open']
        signals['close'] = data_index_int.loc[:, 'close']
        signals['high'] = data_index_int.loc[:, 'high']
        signals['low'] = data_index_int.loc[:, 'low']

        # Initialize the Signal column with "Hold"
        signals['Signal'] = 'Hold'
        signals['Cause'] = 'NA'
        signals['SL'] = np.nan
        signals['TP'] = np.nan

        position = "out"
        stop_loss_price = None
        take_profit_price = None

        # Bullish FVG (1)
        # Take previous -1 high, and +1 low, this gives us the gap to be filled
        # From this, if the -1 high is break, then BUY, otherwise do nothing
        # Keep this support til we are still on the same uptrend
        # If trend change -> reset everything

        bullish_fvg = []

        for index, row in signals[1:].iterrows():
            # Clean FVG not anymore interesting
            bullish_fvg = self._clean_list_by_retention(bullish_fvg, index)

            if position == "out" and signals['FVG'][index] == 1:
                previous_high = signals.loc[index - 1, 'high']
                next_low = signals.loc[index + 1, 'low']

                fvg_item = (index, previous_high, next_low)
                fvg_size = (next_low - previous_high) * 100 / signals.loc[index, 'close']
                if fvg_size > self.FVG_min_size:
                    bullish_fvg.append(fvg_item)
                    logger.debug(f"Adding new FVG entry: {(index, previous_high, next_low)}")
                else:
                    logger.debug(f"FVG Signal is {fvg_size} <= {self.FVG_min_size}")

            elif position == "out" and len(bullish_fvg) > 0:
                for bullish in bullish_fvg:
                    # Loop over current FVG still in list
                    if signals.loc[index, 'close'] < bullish[2]:
                        signals.loc[index, 'Signal'] = 'Buy'
                        signals.loc[index, 'Cause'] = 'FVG Algorithm'
                        position = "in"
                        stop_loss_price = signals.loc[index, 'close'] * (1 - self.stop_loss)
                        take_profit_price = signals.loc[index, 'close'] * (1 + self.take_profit)
                        signals.loc[index, 'SL'] = stop_loss_price
                        signals.loc[index, 'TP'] = take_profit_price
                        bullish_fvg.remove(bullish)
                        break
            elif position == "in":
                if signals.loc[index, 'close'] <= stop_loss_price:
                    signals.loc[index, 'Signal'] = 'Sell'
                    signals.loc[index, 'Cause'] = 'Stop Loss'
                    position = "out"
                elif signals.loc[index, 'close'] >= take_profit_price:
                    signals.loc[index, 'Signal'] = 'Sell'
                    signals.loc[index, 'Cause'] = 'Take Profit'
                    position = "out"

        return signals

    def _clean_list_by_retention(self, l, current_index):
        for i in l:
            if i[0] + self.retention_period < current_index:
                logger.debug(f"Clearing item from the list: {i}")
                l.remove(i)

        return l

    def run_backtest(self):
        """
        Run backtesting for the trading strategy.

        This method initializes a backtest instance with generated signals and historical market data,
        then runs the backtest.

        Returns:
        - backtest_results: Results of the backtest.
        """
        self.backtest = self.backtest_strategy_class(signals=self.generate_signals(), data=self.data)
        return self.backtest.run_backtest()
