import logging

from core.backtest.Backtest import Backtest
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class BacktestLong(Backtest):
    """
    Class for backtesting trading core.
    """

    def __init__(self, signals, data, capital=1000, trade_percentage=0.02):
        """
        Initialize the backtest with a trading strategy, historical market data,
        capital amount, percentage of capital for each trade, stop loss, and take profit.

        Args:
        - signals (DataFrame): The dataframe of all signals (Buy, Sell, Hold)
        - data (DataFrame): Historical market data.
        - capital (float): Initial capital amount.
        - trade_percentage (float): Percentage of capital to allocate for each trade.
        """
        self.signals = signals
        self.data = data
        self.capital = capital
        self.trade_percentage = trade_percentage
        self.entry_points = {}  # Dictionary to store entry points
        self.exit_points = {}  # Dictionary to store exit points

    def run_backtest(self):
        """
        Run the backtest using the provided strategy.

        Returns:
        - performance (dict): Dictionary containing performance metrics.
        """
        # Initialize variables for tracking positions and capital
        position = None
        total_trades = 0
        capital = self.capital
        entry_price = None
        position_size = None

        # Iterate over each row in the signals DataFrame
        for index, row in self.signals.iterrows():
            # print(row)
            # Calculate position size based on trade percentage of capital
            if position is None:
                position_size = capital * self.trade_percentage

            # If the signal is 'Buy' and no position is currently held
            if row['Signal'] == 'Buy' and position is None:
                position = 'Long'
                total_trades += 1
                entry_price = self.data.loc[index + 1, 'open']  # Get the open price of the next tick as entry price
                self.entry_points[index + 1] = entry_price  # Store entry point
                capital -= position_size  # Reduce capital for purchase
                logger.debug(
                    f"Buying at {entry_price} for {position_size} capital is now: {capital}. SL at: {row['SL']} "
                    f"and TP at {row['TP']}")

            # If the signal is 'Sell' and a long position is currently held
            elif row['Signal'] == 'Sell' and position == 'Long':
                position = None
                exit_price = self.data.loc[index + 1, 'open']  # Get the open price of the next tick as exit price
                capital += (position_size * exit_price) / entry_price  # Increase capital for sale
                self.exit_points[index + 1] = exit_price  # Store exit point
                total_trades += 1
                logger.debug(f"Cause: {row['Cause']}. Selling at {exit_price}, capital is now: {capital}")

        # Calculate final performance metrics

        # If we have an open trade, put back the position_size to have complete buy/sell signals
        if position is not None:
            capital += position_size

        final_value = capital
        total_profit = final_value - self.capital

        # Calculate basic performance metrics
        total_trades = len(self.signals)
        buy_signals = (self.signals['Signal'] == 'Buy').sum()
        sell_signals = (self.signals['Signal'] == 'Sell').sum()
        hold_signals = (self.signals['Signal'] == 'Hold').sum()

        performance = {
            'Total Trades': total_trades,
            'Buy Signals': buy_signals,
            'Sell Signals': sell_signals,
            'Hold Signals': hold_signals,
            'Final Value': final_value,
            'Total Profit': total_profit
        }

        return performance

    def plot_backtest(self):
        """
        Plot the backtest results on the historical market data.
        """
        fig, (ax1) = plt.subplots(1, 1, figsize=(12, 8))

        # Plot the historical market data
        ax1.plot(self.data.index, self.data['close'], label='Close Price', color='black')
        ax1.plot(self.data.index, self.data['open'], label='Open Price', color='grey')
        ax1.scatter(self.entry_points.keys(), self.entry_points.values(), color='g', label='Entry Point')
        ax1.scatter(self.exit_points.keys(), self.exit_points.values(), color='r', label='Exit Point')
        ax1.set_ylabel('Price')
        ax1.legend()

        plt.show()
