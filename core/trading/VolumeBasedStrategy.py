import pandas as pd
import numpy as np

from core.trading.Strategy import TradingStrategy


class VolumeBasedStrategy(TradingStrategy):
    """
    Implementation of a volume-based trading strategy.
    """

    def __init__(self, data, volume_threshold=1.5):
        """
        Initialize the trading strategy with historical market data.

        Args:
        - data (DataFrame): Historical market data.
        - volume_threshold (float): Threshold to trigger buy signals based on volume.
        """
        super().__init__(data)
        self.volume_threshold = volume_threshold

    def generate_signals(self):
        """
        Generate buy/sell signals based on volume threshold.

        Returns:
        - signals (DataFrame): DataFrame containing buy/sell signals.
        """
        signals = pd.DataFrame(index=self.data.index)
        signals['volume'] = self.data['volume']

        # Calculate historical average volume
        historical_avg_volume = signals['volume'].mean()

        # Generate buy signals when volume exceeds the threshold
        signals['Signal'] = np.where(signals['volume'] > self.volume_threshold * historical_avg_volume,
                                     'Buy', 'Hold')

        return signals
