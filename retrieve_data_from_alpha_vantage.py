# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests

from config import ALPHA_VANTAGE_API_KEY

symbol = 'SOP.PAR'  # Example stock symbol (replace with Euronext symbol)
outputsize = "compact"

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}&apikey={ALPHA_VANTAGE_API_KEY}&datatype=csv'

print(url)

