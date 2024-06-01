import numpy as np
import pandas as pd

from core.trading.Strategy import TradingStrategy


class RandomStrategy(TradingStrategy):
    """
    Implementation of a simple backtest strategy that generates random buy/sell signals.
    """

    def run_backtest(self):
        self.backtest = self.backtest_strategy_class(signals=self.generate_signals(), data=self.data)
        return self.backtest.run_backtest()

    def __init__(self, data, backtest_strategy_class):
        """
        Initialize the trading strategy with historical market data.

        Args:
        - data (DataFrame): Historical market data.
        """
        super().__init__(data, backtest_strategy_class)

    def generate_signals(self):
        """
        Generate random buy/sell signals.

        Returns:
        - signals (DataFrame): DataFrame containing buy/sell signals.
        """
        np.random.seed(123)  # Set seed for reproducibility
        signals = pd.DataFrame(index=self.data.index)
        signals['Signal'] = np.random.choice(['Buy', 'Sell', 'Hold'], size=len(signals))

        return signals
