from config import XTB_ACCOUNT_DEMO, XTB_PASSWORD_DEMO
from core.connectors.xAPIConnector import *
from core.loaders.xtbLoader import XTBLoader
import logging

logger = logging.getLogger("custom")
logger.setLevel(logging.DEBUG)

# enter your login credentials here
userId = XTB_ACCOUNT_DEMO
password = XTB_PASSWORD_DEMO

with XTBLoader(userId, password) as loader:
    # df = loader.get_data_range(symbol="SOP.FR_9",
    #                           period=1440)
    df = loader.get_data_in_chunks(symbol="SOP.FR_9", period=1, start_timestamp=1086559200000,
                                   end_timestamp=1816501600000)
    loader.write_as_csv(df, symbol="SOP.FR_9", period=1)

# # create & connect to Streaming socket with given ssID
# # and functions for processing ticks, trades, profit and tradeStatus
# sclient = APIStreamClient(ssId=ssid, tickFun=procTickExample, tradeFun=procTradeExample,
#                           profitFun=procProfitExample, tradeStatusFun=procTradeStatusExample)
#
# # subscribe for trades
# sclient.subscribeTrades()
#
# # subscribe for prices
# sclient.subscribePrices(['EURUSD', 'EURGBP', 'EURJPY'])
#
# # subscribe for profits
# sclient.subscribeProfits()
#
# # this is an example, make it run for 5 seconds
# time.sleep(5)
#
# # gracefully close streaming socket
# sclient.disconnect()
