from abc import ABC, abstractmethod
import csv
from datetime import datetime
import logging

from core.utils.CsvReader import CsvReader

logger = logging.getLogger(__name__)


class StrategyEvaluator(ABC):

    def __init__(self, broker, symbol, period):
        """
        Initializes the StrategyEvaluator with the given broker, symbol, and period. Loads the data.

        Parameters:
        -----------
        broker : str
            The name of the broker.
        symbol : str
            The trading symbol.
        period : str
            The period for the trading data.
        """
        self.result = None
        self.broker = broker
        self.symbol = symbol
        self.period = period
        self.data = self._get_data()

    def _get_data(self):
        """
        Reads the trading data from a CSV file based on the broker, symbol, and period, and returns
        it as a pandas DataFrame.

        Returns:
        --------
        pandas.DataFrame
            A DataFrame containing the trading data.
        """
        filepath = f"data/{self.broker}/{self.symbol}_{self.period}.csv"
        reader = CsvReader(filepath)
        return reader.getDataframe()

    @abstractmethod
    def evaluate_strategy(self, params):
        """
        Evaluates the trading strategy based on the provided parameters.

        Parameters:
        -----------
        params : dict
            A dictionary of parameters for the trading strategy.
        """
        pass

    @abstractmethod
    def grid_search(self, params):
        """
        Performs a grid search over a parameter space to find the best parameters for the trading strategy.

        Parameters:
        -----------
        params : dict
            A dictionary of parameter ranges for the grid search.
        """
        pass

    def save_results(self, filename):
        """
        Saves the grid search results to a CSV file.

        Parameters:
        -----------
        filename: str
            The name of the CSV file to save the results.
        """
        if self.result is None:
            logger.error("You can't save any results if the StrategyEvaluator has not been run !")
            return

        version_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(
                ['Strategy', 'Broker', 'Symbol', 'Period', 'Profit', 'Performance Metrics', 'Parameters', 'Version'])

            # Write the data
            for result in self.result:
                class_name, profit, performance_metrics, parameters = result
                writer.writerow([class_name, self.broker, self.symbol, self.period,
                                 profit, performance_metrics, parameters, version_timestamp])
