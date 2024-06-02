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
                 min_number_consecutive=1,
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
        assert (not (merge_consecutive_fvg_start and merge_consecutive_fvg_end) and min_number_consecutive > 1) or (
                (merge_consecutive_fvg_start or merge_consecutive_fvg_end) and min_number_consecutive == 1
        )
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.merge_consecutive_fvg_start = merge_consecutive_fvg_start
        self.merge_consecutive_fvg_end = merge_consecutive_fvg_end
        self.retention_period = retention_period
        self.FVG_min_size = FVG_min_size
        self.min_number_consecutive = min_number_consecutive
        self.bullish_fvg = []

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
        signals['Top'] = fvg_values_index_int['Top']
        signals['Bottom'] = fvg_values_index_int['Bottom']
        signals['RankFVG'] = fvg_values_index_int['RankFVG']

        # Initialize the Signal column with "Hold"
        signals['Signal'] = 'Hold'
        signals['Cause'] = 'NA'
        signals['SL'] = np.nan
        signals['TP'] = np.nan

        position = "out"
        stop_loss_price = None
        take_profit_price = None

        self.bullish_fvg = []

        for index, row in signals[1:].iterrows():
            # Clean FVG not anymore interesting
            self._clean_list(index, signals)

            if position == "out" and signals['FVG'][index] == 1:
                logger.debug(f"Signal for date: {signals['date'][index]}")

                if self._is_FVG_relevant(row):
                    self._append_to_bullish_fvg_list(index, signals)

            elif position == "out" and len(self.bullish_fvg) > 0:
                for bullish in self.bullish_fvg:
                    # Loop over current FVG still in list
                    if signals.loc[index, 'close'] < bullish[2]:
                        signals.loc[index, 'Signal'] = 'Buy'
                        signals.loc[index, 'Cause'] = 'FVG Algorithm'
                        position = "in"
                        stop_loss_price = signals.loc[index, 'close'] * (1 - self.stop_loss)
                        take_profit_price = signals.loc[index, 'close'] * (1 + self.take_profit)
                        signals.loc[index, 'SL'] = stop_loss_price
                        signals.loc[index, 'TP'] = take_profit_price
                        self.bullish_fvg.remove(bullish)
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

    def _append_to_bullish_fvg_list(self, index, signals):
        """

        :param index:
        :param signals:
        :return:
        """
        if signals['RankFVG'][index] == self.min_number_consecutive:
            fvg_item = (index, signals['Bottom'][index - 1], signals['Top'][index - 1])
            self.bullish_fvg.append(fvg_item)
            logger.debug(
                f"Adding new FVG entry: {(index - 1, signals['Bottom'][index - 1], signals['Top'][index - 1])}")
        else:
            logger.debug(f"FVG has already been added to the list.")

    def _is_FVG_relevant(self, row):
        """

        :param row:
        :return:
        """
        fvg_size = (row.Top - row.Bottom) * 100 / row.close
        logger.debug(f"FVG Signal is of size: {fvg_size}")
        if not (fvg_size > self.FVG_min_size):
            logger.debug(f"FVG Signal is {fvg_size} <= {self.FVG_min_size}")
            return False

        # Check rank
        if row.RankFVG < self.min_number_consecutive:
            logger.debug(f"FVG Signal is of rank {row.RankFVG} < {self.min_number_consecutive}")
            return False

        return True

    def _clean_list(self, current_index, signals):
        """
        Clean list depending on the following:
            - Retention period
            - Does the FVG signal have more than X consecutive FVGs
        :param l:
        :param current_index:
        :return:
        """
        for i in self.bullish_fvg:
            if i[0] + self.retention_period < current_index:
                logger.debug(f"Clearing item from the list: {i} because of the retention period.")
                self.bullish_fvg.remove(i)
                continue

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
