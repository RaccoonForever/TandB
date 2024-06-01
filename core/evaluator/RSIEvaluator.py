import logging

from core.backtest import BacktestRSI
from core.evaluator.StrategyEvaluator import StrategyEvaluator
from core.trading import RSIBasedStrategy

logger = logging.getLogger(__name__)


class RSIEvaluator(StrategyEvaluator):
    """
    Evaluates the performance of a trading strategy based on RSI indicators.
    """

    def __init__(self, broker, symbol, period):
        """
        Initializes the RSIEvaluator with the given data.
        """
        super().__init__(broker, symbol, period)

    def grid_search(self, params, top_n=1):
        """
        Performs a grid search over the given parameter ranges to find the top N
        best-performing parameter sets for the RSI-based trading strategy.

        Parameters:
        params (dict): A dictionary containing parameter ranges for the grid search.
            - stop_loss_values (list): List of stop-loss values to test.
            - take_profit_values (list): List of take-profit values to test.
            - rsi_window_values (list): List of RSI window periods to test.
            - overbought_threshold_values (list): List of overbought threshold values to test.
            - oversold_threshold_values (list): List of oversold threshold values to test.
        top_n (int): The number of top performances to keep track of (default is 1).

        Returns:
        list: A list of tuples containing the top N performances and their corresponding parameters.
            Each tuple is in the format (performance, parameters), where:
            - profit (float): The total profit achieved with the given parameters.
            - performances (dict): The different metrics that achieved the performance.
            - parameters (dict): The parameter set that achieved the performance.
        """
        stop_loss_values = params['stop_loss_values']
        take_profit_values = params['take_profit_values']
        rsi_window_values = params['rsi_window_values']
        overbought_threshold_values = params['overbought_threshold_values']
        oversold_threshold_values = params['oversold_threshold_values']

        # Initialize a list to store the top N performances and their parameters
        top_performances = []

        for stop_loss in stop_loss_values:
            for take_profit in take_profit_values:
                for rsi_window in rsi_window_values:
                    for overbought_threshold in overbought_threshold_values:
                        for oversold_threshold in oversold_threshold_values:
                            current_params = {
                                "stop_loss": stop_loss,
                                "take_profit": take_profit,
                                "rsi_window": rsi_window,
                                "overbought_threshold": overbought_threshold,
                                "oversold_threshold": oversold_threshold
                            }
                            performances = self.evaluate_strategy(current_params)
                            profit = performances['Total Profit']

                            # Add the current performance and parameters to the list
                            top_performances.append(
                                (RSIBasedStrategy.__name__, profit, performances, current_params))
                            # Sort the list by performance in descending order
                            top_performances.sort(key=lambda x: x[1], reverse=True)
                            # Keep only the top N performances
                            top_performances = top_performances[:top_n]

        self.result = top_performances
        return top_performances

    def evaluate_strategy(self, params):
        stop_loss = params['stop_loss']
        take_profit = params['take_profit']
        rsi_window = params['rsi_window']
        overbought_threshold = params['overbought_threshold']
        oversold_threshold = params['oversold_threshold']

        logger.info(f"Evaluating RSIBasedStrategy with parameters: {params}")

        strategy = RSIBasedStrategy(data=self.data, backtest_strategy_class=BacktestRSI, rsi_window=rsi_window,
                                    overbought_threshold=overbought_threshold,
                                    oversold_threshold=oversold_threshold,
                                    stop_loss=stop_loss,
                                    take_profit=take_profit)
        return strategy.run_backtest()
