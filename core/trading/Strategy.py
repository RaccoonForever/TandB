from abc import ABC, abstractmethod
import mplfinance as mpf
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class TradingStrategy(ABC):
    """
    Abstract base class for trading core.
    """

    @abstractmethod
    def __init__(self, data, backtest_strategy_class):
        """
        Initialize the trading strategy with historical market data.

        Args:
        - data (DataFrame): Historical market data.
        - backtest_strategy (BacktestStrategy Class): The backtesting strategy to use
        """
        self.data = data
        self.backtest_strategy_class = backtest_strategy_class
        self.backtest = None

    @abstractmethod
    def generate_signals(self):
        """
        Generate trading signals based on the implemented strategy.

        Returns:
        - signals (DataFrame): DataFrame containing buy/sell signals.
        """
        pass

    @abstractmethod
    def run_backtest(self):
        """
        Run the backtest using the provided strategy.

        This method executes the backtesting process by calling the `run_backtest` method of the
        backtest strategy object (`backtest_strategy`). The backtest strategy object should be
        set prior to calling this method.
        """
        pass

    def plot_backtest_with_signals(self):
        return self.backtest.plot_backtest()

    def plot_data_with_signals_v1(self):
        """
        Plot the historical market data along with buy/sell signals.
        """
        signals = self.generate_signals()

        plt.figure(figsize=(12, 6))

        # Plot the closing prices
        plt.plot(self.data.index, self.data['close'], label='Close Price', color='black')

        # Plot buy signals
        plt.plot(signals[signals['Signal'] == 'Buy'].index,
                 self.data.loc[signals['Signal'] == 'Buy', 'close'],
                 '^', markersize=10, color='g', label='Buy Signal')

        # Plot sell signals
        plt.plot(signals[signals['Signal'] == 'Sell'].index,
                 self.data.loc[signals['Signal'] == 'Sell', 'close'],
                 'v', markersize=10, color='r', label='Sell Signal')

        plt.title('Trading Strategy Signals')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

    def plot_data_with_signals_v2(self):
        """
        Plot the historical market data along with buy/sell signals.
        """
        signals = self.generate_signals()

        # print(signals)

        signals_and_data = self.data.copy()
        signals.set_index(self.data.index, inplace=True)
        signals_and_data = signals_and_data.assign(Signal=signals.loc[:, 'Signal'])

        # Create a DataFrame for the signals with a boolean mask
        buy_signals = np.where((signals_and_data['Signal'] == 'Buy'), 1, np.nan) * signals_and_data['low']
        sell_signals = np.where((signals_and_data['Signal'] == 'Sell'), 1, np.nan) * signals_and_data['low']

        markers = []

        # Define the colors for the buy and sell signals
        if not buy_signals.dropna().empty:
            buy_marker = mpf.make_addplot(buy_signals.shift(1), type='scatter', markersize=100, marker='^', color='g')
            markers.append(buy_marker)
        if not sell_signals.dropna().empty:
            sell_marker = mpf.make_addplot(sell_signals.shift(1), type='scatter', markersize=100, marker='v', color='r')
            markers.append(sell_marker)

        # Plot the candlestick chart with buy/sell signals
        mpf.plot(self.data, type='candle', style='charles', addplot=markers,
                 title=self.__class__.__name__, ylabel='Price')
