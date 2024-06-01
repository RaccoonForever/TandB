from abc import ABC, abstractmethod


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
