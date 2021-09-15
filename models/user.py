# import logging 
import primitives.fromJson
import primitives.cipher
import primitives.dca_1

from pprint import pprint

class Adapter:

    def __init__(self, user_name, exchange_name):

        self.un = user_name
        self.en = exchange_name
        self.data = primitives.fromJson.load(f'../../data/users/{user_name}/config.json')
        temp_keys = primitives.cipher.decrypt(f'../../data/users/{user_name}/_{user_name}.bin', self.data['exchanges'][exchange_name.lower()]['ln'])
        key_secret = {'key': temp_keys[-2], 'secret': temp_keys[-1]}
        if len(temp_keys) == 3:
            key_secret.update({'user': temp_keys[0]})
        temp_exchange = __import__(exchange_name)
        self.exchange = temp_exchange.Adapter(self.data['pairs'], **key_secret)

        # self.balances = self.exchange.balances()
        # self.infos = self.exchange.pairsInfo(self.data['pairs'])

    def balances(self, currencies=None):  
        '''On Binance omitting parameter "currencies" returns all that are above 0'''
        return self.exchange.balances(currencies=currencies) # works (only?) on Binance
        # return self.exchange.balances(currencies=self.data['currencies']) # works for Bitstamp

    def orders(self, pairs_list=None):
        return self.exchange.orders(pairs_list)

    def orderBook(self, pair):
        return self.exchange.orderBook(pair)

    def marketOrder(self, pair, side, amount):
        return self.exchange.marketOrder(pair, side, amount)
        
    def limitOrder(self, price, pair, side, amount):
        return self.exchange.limitOrder(price, pair, side, amount)

    def cancelOrder(self, pair, order_id=None, all_orders=False):
        self.exchange.cancelOrder(pair, order_id, all_orders)

    def splatterLimits(self, pair, side, low, high, amount):
        function = primitives.dca_1.buy if side == 'buy' else primitives.dca_1.sell
        infos = self.exchange.infos[pair]
        temp_price = high if side == 'buy' else low
        actual_min_order = self.exchange.calculateMinOrder(pair=pair, price=temp_price)
        if low < float(infos['min_price']) or high > float(infos['max_price']):  # floats unnecessary?
            print('WRONG PRICE RANGE, exiting...') 
            return 
        orders = function(
                low=low, 
                high=high, 
                min_order=infos['min_order'],
                # min_quote_order=infos['min_quote_order'],
                actual_min_order=actual_min_order, 
                min_step=infos['min_price'], 
                amount=amount, 
                max_orders=infos['max_num_orders']/2)
        # return orders  # for testing without placing real orders uncomment this and comment following 2 lines
        for o in orders:
            self.limitOrder(price=o[1], pair=pair, side=side, amount=o[2])

    def crawlingStopLimit(self):
        pass


if __name__ == '__main__':
    # test = Adapter('m', 'Bitstamp')
    test = Adapter('j', 'Binance')
    # print(test.__dict__) 

    # test.balances()
    # pprint(test.orderBook('link_eth'))
    # pprint(test.orderBook('eth_eur'))
    # test.marketOrder(pair='link_eth', side='buy', amount=1.5)
    # test.marketOrder(pair='eth_eur', side='sell', amount=0.2)
    # test.marketOrder(pair='eth_eur', side='sell', amount=0.006)
    pprint(test.balances())
    pprint(test.exchange.infos)
    # pprint(test.limitOrder(0.0006357, 'ada_eth', 'buy', 7.9))
    # pprint(test.cancelOrder('eth_usdt', all_orders=True))
    # pprint(test.cancelOrder('eth_usdt', all_orders=True))
    # pprint(test.cancelOrder('eth_ada', all_orders=True))
    pprint(test.splatterLimits(low=4400, high=12000, pair='eth_usdt', side='sell', amount=0.11572191/2))
    # pprint(test.splatterLimits(low=0.0002, high=0.0006357, pair='ada_eth', side='buy', amount=0.11572191/2))
    # pprint(test.orders(["ada_eth"]))
    # pprint(test.balances(currencies=test.data['currencies'])) # bitsamp only?
    # pprint(test.orders(["ada_usdt", "ada_eth", "link_eth"]))
    # print(logging.root.manager.loggerDict)
