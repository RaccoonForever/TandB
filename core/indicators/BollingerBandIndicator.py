import talib

from core.indicators.Indicator import Indicator


class BollingerBandIndicator(Indicator):

    def __init__(self, data, timeperiod, nbdevup, nbdevdn, matype):
        """
        Initializes the BollingerBandIndicator.

        :param data: list or np.ndarray
            The input data, typically the closing prices of a financial instrument.
        :param timeperiod: int
            The number of periods to use in calculating the moving average and the standard deviation
        :param nbdevup: float
            The number of standard deviations to use for the upper band.
        :param nbdevdn: float
            The number of standard deviations to use for the lower band.
        :param matype: int
            The type of moving average to use
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
        self.nbdevup = nbdevup
        self.nbdevdn = nbdevdn
        self.matype = matype

    def calculate(self):
        """
            Calculate the Bollinger Bands
        """
        return talib.BBANDS(self.data['close'],
                            timeperiod=self.timeperiod,
                            nbdevup=self.nbdevup,
                            nbdevdn=self.nbdevdn,
                            matype=self.matype
                            )
