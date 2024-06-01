import requests
import pandas as pd
import csv


class AlphaVantageAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    # def get_intraday_data(self, symbol, interval='5min', outputsize='compact'):
    #     """
    #     Retrieve intraday stock data from Alpha Vantage.
    #
    #     Args:
    #     - symbol (str): The stock symbol (e.g., AAPL for Apple Inc.).
    #     - interval (str): The time interval between data points (default is '5min').
    #     - outputsize (str): The size of the output data ('compact' or 'full').
    #
    #     Returns:
    #     - data (DataFrame): DataFrame containing the intraday stock data.
    #     """
    #     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={self.api_key}'
    #     response = requests.get(url)
    #     data = response.json()
    #
    #     if 'Time Series (5min)' in data:
    #         data = pd.DataFrame(data['Time Series (5min)']).T
    #         data.index = pd.to_datetime(data.index)
    #         data.columns = ['open', 'high', 'low', 'close', 'volume']
    #         data = data.astype(float)
    #         return data
    #     else:
    #         print("Error: Data not available.")
    #         return None

    def get_daily_data(self, symbol):
        """
        Retrieve daily stock data from Alpha Vantage.

        Args:
        - symbol (str): The stock symbol (e.g., AAPL for Apple Inc.).

        Returns:
        - data (DataFrame): DataFrame containing the daily stock data.
        """
        # First we need to check if the data has already been retrieved
        csv_exist = True
        try:
            df_origin = pd.read_csv(f"data/daily_{symbol}.csv")
        except:
            print("File not existing, let's retrieve all the data.")
            csv_exist = False

        if csv_exist:
            outputsize = "compact"

            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}' \
                  f'&apikey={self.api_key}&datatype=csv'

            with requests.Session() as s:
                download = s.get(url)

                decoded_content = download.text

                with open(f'data/temp/temp_daily_{symbol}.csv', 'w') as f:
                    f.write(decoded_content)

            df_temp = pd.read_csv(f'data/temp/temp_daily_{symbol}.csv')

            df_result = pd.concat([df_origin, df_temp]).drop_duplicates().sort_values(
                "timestamp")
            df_result.to_csv(f"data/daily_{symbol}.csv", index=False)

        else:
            outputsize = "full"

            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}' \
                  f'&apikey={self.api_key}&datatype=csv'

            with requests.Session() as s:
                download = s.get(url)

                decoded_content = download.text.replace("\\\n\\\n", "\\n")

                with open(f'data/daily_{symbol}.csv', 'w') as f:
                    f.write(decoded_content)
