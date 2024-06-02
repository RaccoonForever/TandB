from core.backtest.BacktestLong import BacktestLong
import matplotlib.pyplot as plt


class BacktestFVG(BacktestLong):
    """
    Class for backtesting specific to FVG
    """

    def plot_backtest(self):
        """
        Plot the backtest results on the historical market data.
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

        # Plot the historical market data
        ax1.plot(self.data.index, self.data['close'], label='Close Price', color='black')
        ax1.plot(self.data.index, self.data['open'], label='Open Price', color='grey')
        ax1.scatter(self.entry_points.keys(), self.entry_points.values(), color='g', label='Entry Point')
        ax1.scatter(self.exit_points.keys(), self.exit_points.values(), color='r', label='Exit Point')
        ax1.set_ylabel('Price')
        ax1.legend()

        plt.show()
