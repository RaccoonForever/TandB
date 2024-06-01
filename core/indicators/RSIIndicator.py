from core.indicators.Indicator import Indicator
import talib


class RSIIndicator(Indicator):
    """
    Class for calculating the Relative Strength Index (RSI) indicator.
    """

    def __init__(self, data, window=14):
        """
        Initialize the RSI indicator with historical market data and window size.

        Args:
        - data (DataFrame): Historical market data.
        - window (int): Window size for RSI calculation (default is 14).
        """
        self.data = data
        self.window = window

    def calculate(self):
        """
        Calculate the Relative Strength Index (RSI) indicator.

        Returns:
        - rsi (Series): Series containing RSI values.
        """
        return talib.RSI(self.data['close'], timeperiod=self.window)
