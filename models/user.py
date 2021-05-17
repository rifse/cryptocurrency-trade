import primitives.fromJson
import primitives.cipher

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
        self.exchange = temp_exchange.Adapter(**key_secret)

    def balances(self):
        return self.exchange.balances(self.data['currencies'])

    def orders(self):
        return self.exchange.orders()

    def orderBook(self, pair):
        return self.exchange.orderBook(pair)

    def marketOrder(self, pair, side, amount):
        return self.exchange.marketOrder(pair, side, amount)
        
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
    # test.balances()
    pprint(test.orders(["ada_eth"]))
