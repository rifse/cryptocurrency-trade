from binance.websockets import BinanceSocketManager
import Binance

def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)

client = Binance.Adapter()
bm = BinanceSocketManager(client)

conn_key = bm.start_symbol_ticker_socket('ADAETH', process_message)

bm.start()
