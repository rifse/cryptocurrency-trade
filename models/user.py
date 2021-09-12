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

    # def splatterLimits(self, pair, side, low, high, min_order, min_step, amount):
    def splatterLimits(self, pair, side, low, high, amount):
        function = dca_1.buy if side == 'buy' else dca_1.sell
        # temp_pair = self.exchange.prepareSplatter(pair)
        infos = self.exchange.infos['pair']
        if low < float(infos['min_price']) or high > float(infos['max_price']):
            print('WRONG PRICE RANGE, exiting...') 
            return
        # orders = function(low=low, high=high, min_order=infos['min_order'], min_step=infos['

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
    # pprint(test.limitOrder(4500, 'eth_usdt', 'sell', 0.005))
    # pprint(splatterLimits(
    # pprint(test.orders(["ada_eth"]))
    # pprint(test.balances(currencies=test.data['currencies'])) # bitsamp only?
    # pprint(test.orders(["ada_usdt", "ada_eth", "link_eth"]))
