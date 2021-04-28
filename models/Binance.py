from binance.client import Client
# from binance.websockets import BinanceSocketManager

class Adapter(Client):
    # def __init__(self, api_key=None, api_secret=None):
    #     super().__init__(api_key, api_secret)

    def orderBook(self):
        pass

    def tickers(self):
        return self.get_all_tickers()


if __name__ == '__main__':
    test1 = Adapter()  # user='as'
    # print(test1.tickers())

"""
from binance.websockets import BinanceSocketManager
import Binance

def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)

client = Binance.Adapter()
bm = BinanceSocketManager(client)

conn_key = bm.start_symbol_ticker_socket('ADAETH', process_message)

bm.start()
"""


