import asyncio
import itertools
import json 
import logging.config
import websockets
from socket import gaierror  # , gethostbyname
# from bitstamp.client import Trading
import bitstamp.client
# from primitives.configure_logging import Settings

from pprint import pprint


class Data:

    logger = logging.getLogger('bitstamp')
    print(logger.debug(logging.root.manager.loggerDict))

    # logging.config.dictConfig(Settings.load())
    uri = 'wss://ws.bitstamp.net'
    channels = {'live_trades',} 
    pairs = {'btcusd': {}, 'ethbtc': {}, 'ethusd': {}, 'linketh': {}}

    @classmethod
    def runForever(cls):
        _channels = cls._prepareData()
        while True:
            try:
                asyncio.get_event_loop().run_until_complete(cls._listen(_channels))
            except gaierror:
                cls.logger.debug('!GAIERROR?')
            except KeyboardInterrupt:
                break
            except Exception as e:
                cls.logger.exception(e)

    @classmethod
    async def _listen(cls, data):
        async with websockets.connect(cls.uri, ping_interval=20, ping_timeout=20, close_timeout=10) as websocket:
            for event in data:
                await websocket.send(json.dumps(event))
            while True:
                try:
                    results = await websocket.recv()
                    cls.logger.debug(results)
                    cls._applyChanges(json.loads(results))
                except Exception as e:
                    cls.logger.exception(e)
                    break

    @classmethod
    def _prepareData(cls):
        temp = ['_'.join(ch) for ch in itertools.product(cls.channels, cls.pairs)]
        channels = [{'event': 'bts:subscribe', 'data': {'channel': ch}} for ch in temp]
        return channels 

    @classmethod
    def _applyChanges(cls, data):
        try:
            ch_name = data['channel']
            if ch_name.startswith('live_trades_'):
                try:
                    cls.pairs[ch_name.split('_')[2]] = {'price': data['data']['price'],  # get pair string from channel name
                                                        'type': data['data']['type']}  # 0 == BUY; 1 == SELL
                except KeyError:
                    try:
                        if data['event'].endswith('succeeded'):
                            cls.logger.info(f'successfully connected to {ch_name}')
                        else:
                            cls.logger.info(f'apparently NOT successfully connected to {ch_name}')
                    except KeyError:
                        cls.logger.exception('KEYERROR_2 IN Data._applyChanges')
            else:
                cls.logger.exception('Unknown Channel!?')
        except KeyError:  # AttributeNotFound?
            cls.logger.exception('KEYERROR_1 IN Data._applyChanges')

class Adapter(bitstamp.client.Trading):

    def __init__(self, **kwds):
        kwds['username'] = kwds.pop('user')  # change user to username?
        super().__init__(**kwds)
        # pprint(self.__dict__)

    def balances(self, currencies):  # currencies is a list
        balances = {}
        for c in currencies:
            balances.update({c: self.account_balance(c, "usd")})
        return balances

    def getMinOrder(self, pair):
        # if minorder exists just get it, otherwise following:
        bq = pair.split('_')
        quote = bq[1]
        if quote == 'btc':
            pass
        elif quote == 'eth':
            pass
        elif quote in ['usd', 'eur', 'gbp', 'pax', 'usdc', 'dai']:
            pass
        else:
            raise ValueError('Wrong pair format!')

    def orders(self, pairs=None):
        return self.user_transactions()

    def orderBook(self, pair):
        bq = pair.split('_')
        return self.order_book(base=bq[0], quote=bq[1])

    def marketOrder(self, pair, side, amount):
        bq = pair.split('_')
        function = self.buy_market_order if side == 'buy' else self.sell_market_order
        return function(amount=amount, base=bq[0], quote=bq[1])


if __name__ == '__main__':
    Data.runForever()
    # a = Adapter().ticker()
    # print(a)
