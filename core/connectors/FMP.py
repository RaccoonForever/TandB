import requests


class FMPApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://financialmodelingprep.com/api/v3"

    def _make_request(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}&apikey={self.api_key}")
        response.raise_for_status()
        return response.json()

    def get_historical_chart(self, symbol, timeframe, from_date, to_date):
        endpoint = f"historical-chart/{timeframe}/{symbol}?from={from_date}&to={to_date}"
        return self._make_request(endpoint)
