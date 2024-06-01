from config import FMP_API_KEY
from core.connectors.FMP import FMPApi
import logging

logger = logging.getLogger("custom")
logger.setLevel(logging.DEBUG)

fmpClient = FMPApi(api_key=FMP_API_KEY)

print(fmpClient.get_historical_chart(
    symbol="SOP.PA",
    timeframe="1hour",
    from_date="2019-01-01",
    to_date="2023-01-01"
))