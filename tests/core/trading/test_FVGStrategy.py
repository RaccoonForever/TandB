import unittest
import pandas as pd
import logging

from core.trading.FVGStrategy import FVGBasedStrategy
from core.backtest.BacktestLong import BacktestLong


class TestRSIStrategy(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)

    def test_generateSignals_with_constant_values(self):
        data = pd.read_csv("data/data_constant_values.csv")

        strategy = FVGBasedStrategy(data=data, backtest_strategy_class=BacktestLong)
        signals = strategy.generate_signals()

        self.assertTrue((signals['Signal'] == "Hold").all())

    def test_generateSignals_buy_sell_simple_scenario(self):
        data = pd.read_csv("data/data_fvg_values.csv", index_col=0, parse_dates=True)

        strategy = FVGBasedStrategy(data=data, backtest_strategy_class=BacktestLong,
                                    merge_consecutive_fvg_start=True,
                                    stop_loss=0.01,
                                    take_profit=0.02,
                                    retention_period=10)
        signals = strategy.generate_signals()
        strategy.plot_data_with_signals_v2()

        self.assertEqual(signals.loc[16, 'FVG'], 1.0)
        self.assertEqual(signals.loc[16, 'Signal'], 'Hold')

        self.assertEqual(signals.loc[26, 'Signal'], "Buy")
        self.assertAlmostEqual(signals.loc[26, 'SL'], 159.786, delta=0.0001)
        self.assertAlmostEqual(signals.loc[26, 'TP'], 164.628, delta=0.0001)

        self.assertEqual(signals.loc[34, 'Signal'], 'Sell')
        self.assertEqual(signals.loc[34, 'Cause'], 'Take Profit')

    def test_generateSignals_retention_period_small(self):
        data = pd.read_csv("data/data_fvg_values.csv", index_col=0, parse_dates=True)

        strategy = FVGBasedStrategy(data=data, backtest_strategy_class=BacktestLong,
                                    merge_consecutive_fvg_start=True,
                                    stop_loss=0.01,
                                    take_profit=0.02,
                                    retention_period=1)
        signals = strategy.generate_signals()

        self.assertTrue((signals['Signal'] == "Hold").all())

    def test_generateSignals_buy_sell_simple_scenario_2(self):
        """
        We don't want to have a Buy Signal if the FVG is too small
        """
        data = pd.read_csv("data/data_fvg_values_2.csv", index_col=0, parse_dates=True)

        strategy = FVGBasedStrategy(data=data, backtest_strategy_class=BacktestLong,
                                    merge_consecutive_fvg_start=True,
                                    stop_loss=0.01,
                                    take_profit=0.02,
                                    retention_period=10,
                                    FVG_min_size=0.1)
        signals = strategy.generate_signals()
        print(signals[['date', 'FVG', 'close', 'Cause', 'SL', 'TP', 'Signal']])
        strategy.plot_data_with_signals_v2()
