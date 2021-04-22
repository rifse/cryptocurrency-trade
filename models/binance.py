from binance.client import Client

class Adapter(Client):
    def __init__(self, api_key=None, api_secret=None):
        super().__init__(api_key, api_secret)

    def orderBook(self):
        pass

    def tickers(self):
        return self.get_all_tickers()


if __name__ == '__main__':
    test1 = Adapter()  # user='as'
    # print(test1.tickers())
