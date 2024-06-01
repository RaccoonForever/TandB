import unittest
import pandas as pd

from core.trading.RSIStrategy import RSIBasedStrategy
from core.backtest.BacktestLong import BacktestLong


class TestRSIStrategy(unittest.TestCase):

    def test_generateSignals_with_constant_values(self):
        data = pd.read_csv("data/data_constant_values.csv")

        strategy = RSIBasedStrategy(data=data, backtest_strategy_class=BacktestLong, stop_loss=0.05,
                                    take_profit=0.40)
        signals = strategy.generate_signals()
        print(strategy.generate_signals())

        self.assertTrue(signals[0:14]['RSI'].isnull().all())
        self.assertTrue((signals[14:]['RSI'] == 0.0).all())
        self.assertEqual(signals.iloc[14]['Signal'], "Buy")

    def test_generateSignals_with_alternate_values(self):
        data = pd.read_csv("data/data_2_values.csv")

        strategy = RSIBasedStrategy(data=data, backtest_strategy_class=BacktestLong)
        signals = strategy.generate_signals()
        print(strategy.generate_signals())

        self.assertTrue((signals['Signal'] == "Hold").all())
        self.assertEqual(signals.iloc[14]['Signal'], "Hold")
        self.assertEqual(signals.iloc[14]['RSI'], 50.0)
