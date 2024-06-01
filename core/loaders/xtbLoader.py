import os
import pandas as pd
from datetime import datetime, timedelta

from core.connectors.xAPIConnector import *

import logging

PERIOD_M1 = 1
PERIOD_M5 = 5
PERIOD_M15 = 15
PERIOD_M30 = 30
PERIOD_H1 = 60  # (1 hour)
PERIOD_H4 = 240  # (4 hours)
PERIOD_D1 = 1440  # (1 day)
PERIOD_W1 = 10080  # (1 week)

period_range = {
    PERIOD_M1: timedelta(days=30),
    PERIOD_M5: timedelta(days=30 * 6),
    PERIOD_M15: timedelta(days=365),
    PERIOD_M30: timedelta(days=365 * 2),
    PERIOD_H1: timedelta(days=365 * 4),
    PERIOD_H4: timedelta(days=365 * 10),
    PERIOD_D1: timedelta(days=365 * 20),
    PERIOD_W1: timedelta(days=365 * 20)
}


class XTBLoader:
    path_prefix = "data/XTB"

    def __init__(self, user_id, user_pwd):
        self.user_id = user_id
        self.user_pwd = user_pwd
        self.xtbClient = APIClient()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        loginResponse = self.xtbClient.execute(loginCommand(userId=self.user_id, password=self.user_pwd))
        logger.info(f"XTB Login Response: {str(loginResponse)}")

        # check if user logged in correctly
        if not loginResponse['status']:
            logger.error(f"Login failed. Error code: {loginResponse['errorCode']}")
            raise Exception

    def disconnect(self):
        logging.info("Shutting down gracefully the socket")
        self.xtbClient.disconnect()

    def get_data_in_chunks(self, symbol, period, start_timestamp, end_timestamp):
        """
        Retrieves data for a symbol in chunks by repeatedly calling get_data_range within a loop.

        :param symbol: The asset symbol in XTB.
        :param period: The number of minutes per tick.
        :param start_timestamp: The start time in 13-digit timestamp (milliseconds).
        :param end_timestamp: The end time in 13-digit timestamp (milliseconds).
        :return: A concatenated DataFrame containing the data retrieved in chunks.
        """
        # Convert timestamps to integers if they are not already
        start_timestamp = int(start_timestamp)
        end_timestamp = int(end_timestamp)

        # Initialize an empty DataFrame to store the data
        all_data = pd.DataFrame()

        # Get chunk size based on the period
        chunk_size = int(period_range[period].total_seconds() * 1000)

        current_start = start_timestamp
        while current_start < end_timestamp:
            current_end = min(current_start + chunk_size, end_timestamp)

            print(current_start)
            print(current_end)

            # Fetch data for the current chunk
            chunk_df = self.get_data_range(symbol, period, current_start, current_end)

            # Concatenate the chunk data with all_data
            all_data = pd.concat([all_data, chunk_df], ignore_index=True)

            # Update the start timestamp for the next chunk
            current_start = current_end + 1  # Ensure no overlap

            # Optional: Sleep for a short time to avoid hitting rate limits
            time.sleep(0.1)

        # Drop any potential duplicates
        all_data = all_data.drop_duplicates()

        return all_data

    def get_data_range(self, symbol, period, start_timestamp=None, end_timestamp=None):
        """
            Get the data for a symbol and a period.
            If any start or end timestamp are not specified or are not 13 digits, use now - X time (depending on the
            period chosen)

            :param symbol: the asset symbol in XTB
            :param period: the number of min by tick
                Ex. :

                name	    value	description
                PERIOD_M1	1	    1 minute
                PERIOD_M5	5	    5 minutes
                PERIOD_M15	15	    15 minutes
                PERIOD_M30	30	    30 minutes
                PERIOD_H1	60	    60 minutes (1 hour)
                PERIOD_H4	240	    240 minutes (4 hours)
                PERIOD_D1	1440	1440 minutes (1 day)
                PERIOD_W1	10080	10080 minutes (1 week)
                PERIOD_MN1	43200	43200 minutes (30 days)

            :param start_timestamp: the start time in 13-digit timestamp (milliseconds)
            :param end_timestamp: the end time in 13-digit timestamp (milliseconds)
            :return: the df of the data
        """

        # Get current time in milliseconds
        current_time_ms = int(time.time() * 1000)

        # Default start time (10 years ago in milliseconds)
        default_start_time_ms = int((datetime.now() - period_range[period]).timestamp() * 1000)

        # Validate and set start_timestamp
        if start_timestamp is None or len(str(start_timestamp)) != 13:
            start_timestamp = default_start_time_ms

        # Validate and set end_timestamp
        if end_timestamp is None or len(str(end_timestamp)) != 13:
            end_timestamp = current_time_ms

        # Ensure start_timestamp and end_timestamp are integers
        start_timestamp = int(start_timestamp)
        end_timestamp = int(end_timestamp)

        resp = self.xtbClient.commandExecute('getChartRangeRequest', arguments={
            "info": {
                "end": end_timestamp,
                "period": period,
                "start": start_timestamp,
                "symbol": symbol,
                "ticks": 0
            }
        })

        return self.transform_response_into_df(resp, period)

    def transform_response_into_df(self, response, period):
        """
            Transforms the response data from the XTB client into a pandas DataFrame.

            This method processes the raw response data, extracts relevant fields, formats timestamps,
            adjusts price values based on the number of digits, and organizes the data into a structured
            DataFrame.

            :param response: The raw response data from the XTB client. Expected to contain 'rateInfos' and 'digits'.
            :param period: The period (in minutes) for the data transformation, used to format timestamps.
            :return: A pandas DataFrame containing the transformed data.
        """
        rate_infos = response['returnData']['rateInfos']
        digits = response['returnData']['digits']
        df = pd.DataFrame(rate_infos)
        if df.empty:
            return df

        df['ctmString'] = pd.to_datetime(df['ctmString'], format="%b %d, %Y, %I:%M:%S %p")

        if period == PERIOD_D1:
            df['timestamp'] = df['ctmString'].dt.strftime('%Y-%m-%d')
        elif period < PERIOD_D1:
            df['timestamp'] = df['ctmString'].dt.strftime('%Y-%m-%d %H:%M:%S')

        df['open'] = df['open'] / (10 ** digits)
        df['close'] = df['open'] + (df['close'] / (10 ** digits))
        df['high'] = df['open'] + (df['high'] / (10 ** digits))
        df['low'] = df['open'] + (df['low'] / (10 ** digits))
        df['volume'] = df['vol']
        # Round values in specified columns
        columns_to_round = ['open', 'high', 'low', 'close', 'volume']
        df[columns_to_round] = df[columns_to_round].round(3)

        df.drop(columns=['ctmString', 'ctm', 'vol'], inplace=True)
        df = df[['timestamp', 'open', 'close', 'high', 'low', 'volume']]
        return df

    def write_as_csv(self, df, symbol, period):
        """
            Writes the DataFrame to a CSV file. If the file already exists, it appends new data
            to the existing file, removes duplicates, sorts the data by timestamp, and saves the
            updated DataFrame back to the CSV file.

            :param df: The DataFrame containing the data to be written to the CSV file.
            :param symbol: The asset symbol used in XTB.
            :param period: The period (in minutes) for the data, used in naming the CSV file.
        """
        # Check if the file exists
        filepath = f"{self.path_prefix}/{symbol}_{period}.csv"

        if os.path.exists(filepath):
            # Read existing CSV into DataFrame
            existing_df = pd.read_csv(filepath)
            # Concatenate existing and new data
            df = pd.concat([existing_df, df], ignore_index=True).drop_duplicates()

        # Save DataFrame to CSV
        df.sort_values("timestamp", inplace=True)
        df.to_csv(filepath, index=False)
