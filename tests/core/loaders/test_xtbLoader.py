import unittest
import pandas as pd

from core.loaders.xtbLoader import XTBLoader


class TestXTBLoader(unittest.TestCase):
    def test_daily_parser(self):
        response = {'status': True, 'returnData': {'rateInfos': [
            {'ctm': 1713132000000, 'ctmString': 'Apr 15, 2024, 12:00:00 AM', 'open': 22520.0, 'close': 20.0,
             'high': 280.0, 'low': -60.0, 'vol': 10145.0},
            {'ctm': 1713218400000, 'ctmString': 'Apr 16, 2024, 12:00:00 AM', 'open': 22200.0, 'close': 120.0,
             'high': 180.0, 'low': -200.0, 'vol': 13377.0},
            {'ctm': 1713304800000, 'ctmString': 'Apr 17, 2024, 12:00:00 AM', 'open': 22220.0, 'close': -80.0,
             'high': 180.0, 'low': -160.0, 'vol': 9979.0},
            {'ctm': 1713391200000, 'ctmString': 'Apr 18, 2024, 12:00:00 AM', 'open': 22000.0, 'close': 100.0,
             'high': 140.0, 'low': -260.0, 'vol': 3401.0},
            {'ctm': 1713477600000, 'ctmString': 'Apr 19, 2024, 12:00:00 AM', 'open': 21880.0, 'close': -480.0,
             'high': 0.0, 'low': -480.0, 'vol': 13077.0}, ], 'digits': 2, 'exemode': 1}}

        loader = XTBLoader()
        df = loader.transform_daily_response_into_df(response)

        print(df.iloc[0])

        self.assertAlmostEqual(df.iloc[0]['open'], 225.2, delta=0.001)
        self.assertAlmostEqual(df.iloc[0]['close'], 225.4, delta=0.001)
        self.assertAlmostEqual(df.iloc[0]['high'], 228.0, delta=0.001)
        self.assertAlmostEqual(df.iloc[0]['low'], 224.6, delta=0.001)
        self.assertEqual(df.iloc[0]['timestamp'], "2024-04-15")
        self.assertAlmostEqual(df.iloc[0]['volume'], 10145.0, delta=0.001)
