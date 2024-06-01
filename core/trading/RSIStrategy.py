import pandas as pd
import numpy as np

from core.trading.Strategy import TradingStrategy
from core.indicators.RSIIndicator import RSIIndicator


class RSIBasedStrategy(TradingStrategy):
    """
    Implementation of an RSI-based trading strategy.
    """

    def __init__(self, data, backtest_strategy_class, rsi_window=14, overbought_threshold=70, oversold_threshold=30,
                 stop_loss=None, take_profit=None):
        """
        Initialize the trading strategy with historical market data and RSI parameters.

        Args:
        - data (DataFrame): Historical market data.
        - rsi_window (int): Window size for RSI calculation (default is 14).
        - overbought_threshold (float): Overbought threshold for RSI (default is 70).
        - oversold_threshold (float): Oversold threshold for RSI (default is 30).
        - stop_loss (float or None): Stop loss percentage (e.g., 0.05 for 5%) for exiting a losing trade.
        - take_profit (float or None): Take profit percentage (e.g., 0.1 for 10%) for exiting a winning trade.
        """
        super().__init__(data, backtest_strategy_class)
        self.rsi_window = rsi_window
        self.overbought_threshold = overbought_threshold
        self.oversold_threshold = oversold_threshold
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def generate_signals(self):
        """
        Generate buy/sell signals based on RSI.

        Returns:
        - signals (DataFrame): DataFrame containing buy/sell signals.
        """
        rsi_indicator = RSIIndicator(self.data, window=self.rsi_window)
        rsi_values = rsi_indicator.calculate()
        self.data = self.data.assign(RSI=rsi_values)

        signals = pd.DataFrame(index=self.data.index)
        signals.loc[:, 'RSI'] = rsi_values

        # Initialize the Signal column with "Hold"
        signals['Signal'] = 'Hold'
        signals['Cause'] = 'NA'
        signals['SL'] = np.nan
        signals['TP'] = np.nan

        position = "out"
        stop_loss_price = None
        take_profit_price = None

        for index, row in signals.iterrows():
            if position == "out" and signals['RSI'][index] < self.oversold_threshold:
                signals.loc[index, 'Signal'] = 'Buy'
                signals.loc[index, 'Cause'] = 'RSI Algorithm'
                position = "in"
                entry_price = self.data['close'][index]
                stop_loss_price = entry_price * (1 - self.stop_loss)
                take_profit_price = entry_price * (1 + self.take_profit)
                signals.loc[index, 'SL'] = stop_loss_price
                signals.loc[index, 'TP'] = take_profit_price
            elif position == "in":
                if self.data['close'][index] <= stop_loss_price:
                    signals.loc[index, 'Signal'] = 'Sell'
                    signals.loc[index, 'Cause'] = 'Stop Loss'
                    position = "out"
                elif self.data['close'][index] >= take_profit_price:
                    signals.loc[index, 'Signal'] = 'Sell'
                    signals.loc[index, 'Cause'] = 'Take Profit'
                    position = "out"
                elif signals['RSI'][index] > self.overbought_threshold:
                    signals.loc[index, 'Signal'] = 'Sell'
                    signals.loc[index, 'Cause'] = 'RSI Algorithm'
                    position = "out"

        return signals

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
