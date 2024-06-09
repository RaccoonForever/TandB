from abc import ABC, abstractmethod

from core.utils.contants import SIGNAL_SELL_SHORT, SIGNAL_SELL_LONG


class Backtest(ABC):
    @abstractmethod
    def run_backtest(self):
        """
        Backtest the trading strategy using historical data.

        Returns:
        - performance (dict): Dictionary containing performance metrics.
        """
        pass

    @abstractmethod
    def plot_backtest(self):
        pass

    def get_profit(self, signal, position_size, entry, exit, fee=0):
        if signal == SIGNAL_SELL_LONG:
            return (exit - entry - fee) * position_size
        elif signal == SIGNAL_SELL_SHORT:
            return (entry - exit - fee) * position_size
