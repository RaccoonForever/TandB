import talib
from talib import MA_Type

from core.indicators.Indicator import Indicator


class MovingAverageIndicator(Indicator):

    def __init__(self, data, timeperiod, matype=MA_Type.SMA):
        """
        Initializes the MovingAverageIndicator.

        :param data: list or np.ndarray
            The input data, typically the closing prices of a financial instrument.
        :param timeperiod: int
            The number of periods to use in calculating the moving average.
        :param matype: int
            The type of moving average to use.
                0 is SMA
                1 is EMA
                2 is WMA
                3 is DMA
                4 is TEMA
                5 is TRIMA
                6 is KAMA
                7 is MAMA
                8 is T3
            Check "from talib import MA_Type" for more details
        """
        self.data = data
        self.timeperiod = timeperiod
        self.matype = matype

    def calculate(self):
        """
        Calculate the moving average.
        """
        return talib.MA(self.data['close'], timeperiod=self.timeperiod, matype=self.matype)
