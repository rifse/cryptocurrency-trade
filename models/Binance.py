from binance import Client
from decimal import Decimal
import datetime
# import logging
from pprint import pprint
import math
# from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
# from binance.websockets import BinanceSocketManager

class Adapter(Client):

    def __init__(self, pairs_list, **kwds):
        kwds['api_key'] = kwds.pop('key')  # change user to username?
        kwds['api_secret'] = kwds.pop('secret')  # change user to username?
        super().__init__(**kwds)

        # self.logger = logging.getLogger('requests')
        # print(logger.debug(logging.root.manager.loggerDict))
        self.infos = self.pairsInfo(pairs_list)
        # print(self.ping())

    def balances(self, currencies=None):
        balances = {}
        if currencies:
            for c in currencies:
                b = self.get_asset_balance(asset=c)
                balances.update({b.pop('asset'): b})
        else:
            temp_balances = self.get_account()['balances']
            for b in temp_balances:
                if float(b['free']) > 0 or float(b['locked']) > 0:
                    balances.update({b.pop('asset'): b})
        return balances

    def orders(self, pairs=None):
        orders = {}
        if pairs:
            for p in pairs:
                # now = datetime.datetime.utcnow()
                # endTime = round(datetime.datetime.timestamp(now))
                # startTime = round(datetime.datetime.timestamp(now - datetime.timedelta(days=3000)))
                # orderNumber = 163899572
                symbol = ''.join(p.upper().split('_'))
                orders.update({symbol: self.get_all_orders(symbol=symbol)})
                # self.get_order(symbol=symbol)
                # self.get_all_orders(symbol=symbol, orderId=orderNumber)
                # self.get_all_orders(symbol=symbol, startTime=startTime)
                # self.get_all_orders(symbol=symbol, startTime=startTime, endTime=endTime)
                # self.get_aggregate_trades(symbol=p.split('_').upper().join(''))
                # self.get_historical_trades(symbol=p.split('_').upper().join(''))
                # self.get_recent_trades(symbol=p.split('_').upper().join(''))
                # self.get_order(symbol=p.split('_').upper().join(''))
        return orders

    def pairsInfo(self, pairs_list):
        infos = {}
        temp_pairs = [''.join(p.upper().split('_')) for p in pairs_list]
        res = self.get_exchange_info()
        for item in res['symbols']:
            local_name = item['symbol']
            if local_name in temp_pairs:
                # pprint(item)
                item['filters'] = {x.pop('filterType'): x for x in item['filters']}
                temp_infos = {
                        'local_name': local_name,
                        'min_order': float(item['filters']['LOT_SIZE']['minQty']), 
                        'min_quote_order': float(item['filters']['MIN_NOTIONAL']['minNotional']), 
                        'max_order': float(item['filters']['LOT_SIZE']['maxQty']),
                        'min_price': float(item['filters']['PRICE_FILTER']['minPrice']),
                        'max_price': float(item['filters']['PRICE_FILTER']['maxPrice']),
                        'max_num_orders': int(item['filters']['MAX_NUM_ORDERS']['maxNumOrders'])}
                infos.update({pairs_list[temp_pairs.index(local_name)]: temp_infos})
        return infos

    def orderBook(self):
        pass

    def calculateMinOrder(self, pair, price):
        infos = self.infos[pair]
        decimals = abs(math.floor(math.log(infos['min_order'], 10)))
        return round(max(infos['min_order'], infos['min_quote_order']/price), decimals)

    def tickers(self):
        return self.get_all_tickers()

    def marketOrder(self, pair, side, amount):
        '''Not tested yet!'''
        return self.create_order(
                symbol=''.join(pair.upper().split('_')),
                side=side.upper(),
                type='MARKET',
                timeInForce='GTC',
                quantity=amount)

    def limitOrder(self, price, pair, side, amount):
        '''Not tested yet!'''
        return self.create_order(
                symbol=''.join(pair.upper().split('_')),
                side=side.upper(),
                type='LIMIT',
                timeInForce='GTC',
                quantity=amount,
                # quantity=Decimal(amount),
                price=str(price))

    def cancelOrder(self, pair, order_id=None, all_orders=False):
        # https://github.com/sammchardy/python-binance/issues/533
        # binance_client._delete('openOrders', True, data={'symbol': 'DOGEBTC'})
        pair = ''.join(pair.upper().split('_'))
        if all_orders:
            self._delete('openOrders', True, data={'symbol': pair})
        else:
            if not order_id:
                print('MUST COMMAND all_orders=True OR PROVIDE order_id, exiting..')
            else:
                self.cancel_order(symbol=pair, orderId=order_id)


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
