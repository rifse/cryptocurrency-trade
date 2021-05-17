from binance import Client
# from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
# from binance.websockets import BinanceSocketManager

class Adapter(Client):

    # def __init__(self, api_key=None, api_secret=None):
    def __init__(self, **kwds):
        kwds['api_key'] = kwds.pop('key')  # change user to username?
        kwds['api_secret'] = kwds.pop('secret')  # change user to username?
        super().__init__(**kwds)

    def balances(self, currencies=None):
        return self.get_balance()

    def orders(self, pairs=None):
        for p in pairs:
            self.get_order(symbol=p.split('_').upper().join(''))

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


