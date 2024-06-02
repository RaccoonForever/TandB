import unittest

import numpy as np
import pandas as pd

from core.indicators.FVGIndicator import FVGIndicator


class TestFVGIndicator(unittest.TestCase):

    def test_calculate_with_constant_values(self):
        data = pd.read_csv("data/data_constant_values.csv")

        indicator = FVGIndicator(data)

        result = indicator.calculate().dropna()

        self.assertTrue(result.empty)

    def test_calculate_with_basic_values_and_merge_to_false(self):
        data = pd.read_csv("data/data_fvg_values.csv")

        indicator = FVGIndicator(data)

        result = indicator.calculate()

        self.assertTrue((result.loc[16:18, 'FVG'] == 1).all())
        self.assertTrue((result.loc[23:25, 'FVG'] == -1).all())

    def test_calculate_with_basic_values_and_merge_start(self):
        data = pd.read_csv("data/data_fvg_values.csv")

        indicator = FVGIndicator(data, merge_consecutive_fvg_start=True)

        result = indicator.calculate()

        self.assertEqual(result.loc[16, 'FVG'], 1)
        self.assertTrue(np.isnan(result.loc[17, 'FVG']))
        self.assertTrue(np.isnan(result.loc[18, 'FVG']))
        self.assertEqual(result.loc[16, 'Bottom'], 161.7)
        self.assertEqual(result.loc[16, 'Top'], 164.6)

        self.assertTrue(result.loc[23, 'FVG'] == -1)
        self.assertTrue(np.isnan(result.loc[24, 'FVG']))
        self.assertTrue(np.isnan(result.loc[25, 'FVG']))

    def test_calculate_with_basic_values_and_merge_end(self):
        data = pd.read_csv("data/data_fvg_values.csv")

        indicator = FVGIndicator(data, merge_consecutive_fvg_end=True)

        result = indicator.calculate()

        self.assertTrue(np.isnan(result.loc[16, 'FVG']))
        self.assertTrue(np.isnan(result.loc[17, 'FVG']))
        self.assertEqual(result.loc[18, 'FVG'], 1)

        self.assertTrue(np.isnan(result.loc[23, 'FVG']))
        self.assertTrue(np.isnan(result.loc[24, 'FVG']))
        self.assertTrue(result.loc[25, 'FVG'] == -1)
