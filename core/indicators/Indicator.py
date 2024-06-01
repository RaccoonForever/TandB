from abc import ABC, abstractmethod


class Indicator(ABC):
    """
    Abstract base class for financial indicators.
    """

    @abstractmethod
    def calculate(self):
        """
        Abstract method to calculate the indicator.

        Returns:
        - result: Result of the indicator calculation.
        """
        pass
