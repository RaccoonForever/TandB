import pandas as pd


class CsvReader:

    def __init__(self, path):
        self.file_path = path
        self.df = pd.read_csv(path, index_col=0, parse_dates=True)
        self.reverse_dataframe_if_needed()

    def get_dataframe(self):
        return self.df

    def reverse_dataframe_if_needed(self):
        """
        Reverse the DataFrame if the timestamp of the first row is greater than that of the second row.

        Args:
        - df (DataFrame): Input DataFrame to be reversed.

        Returns:
        - reversed_df (DataFrame): Reversed DataFrame if needed.
        """
        if len(self.df) >= 2 and self.df.index[0] > self.df.index[1]:
            self.df = self.df[::-1]  # Reverse the DataFrame
            self.df.reset_index(inplace=True, drop=True)
