import logging

from core.backtest import BacktestFVG
from core.evaluator.StrategyEvaluator import StrategyEvaluator
from core.trading import FVGBasedStrategy

logger = logging.getLogger(__name__)


class FVGEvaluator(StrategyEvaluator):
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
        retention_period_values = params['retention_period_values']
        FVG_min_size_values = params['FVG_min_size_values']

        # Initialize a list to store the top N performances and their parameters
        top_performances = []

        for stop_loss in stop_loss_values:
            for take_profit in take_profit_values:
                for retention_period in retention_period_values:
                    for min_size in FVG_min_size_values:
                        current_params = {
                            "stop_loss": stop_loss,
                            "take_profit": take_profit,
                            "retention_period": retention_period,
                            "FVG_min_size": min_size
                        }
                        performances = self.evaluate_strategy(current_params)
                        profit = performances['Total Profit']

                        # Add the current performance and parameters to the list
                        top_performances.append(
                            (FVGBasedStrategy.__name__, profit, performances, current_params))
                        # Sort the list by performance in descending order
                        top_performances.sort(key=lambda x: x[1], reverse=True)
                        # Keep only the top N performances
                        top_performances = top_performances[:top_n]

        self.result = top_performances
        return top_performances

    def evaluate_strategy(self, params):
        stop_loss = params['stop_loss']
        take_profit = params['take_profit']
        retention_period = params['retention_period']
        FVG_min_size = params['FVG_min_size']

        logger.info(f"Evaluating FVGBased Strategy with parameters: {params}")

        strategy = FVGBasedStrategy(data=self.data, backtest_strategy_class=BacktestFVG,
                                    merge_consecutive_fvg_start=False,
                                    merge_consecutive_fvg_end=False,
                                    retention_period=retention_period,
                                    FVG_min_size=FVG_min_size,
                                    min_number_consecutive=2,
                                    stop_loss=stop_loss, take_profit=take_profit)
        return strategy.run_backtest()
