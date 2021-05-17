"""Docstring."""
import argparse
import logging
# from math import floor, log
# from pprint import pformat
import time
from keysAndDecryption.decrypt import decrypt

# logging.basicConfig(filename='botov.log', level=logging.INFO,
#                     format='%(asctime)s %(name)s:%(levelname)s:%(message)s')
formatter = logging.Formatter('%(asctime)s %(name)s:%(levelname)s:%(message)s')
logger = logging.getLogger('orderPlacer_LOGGER')
logger.setLevel(logging.INFO)

# BITFINEX_SYMBOL = 'ZRXETH'
# BINANCE_SYMBOL = 'ZRXETH'
# MINSIZE_BITFINEX_ZRX = 20.0
# MINSIZE_BINANCE_ETH = 0.01
# CONSTANT4BITFINEX = float(10**6)


def placeOrder(EXCHANGE, PASSWORD_FILE, ASSET_1, ASSET_2, PRICE, QUANTITY):

    if EXCHANGE == 'bitstamp':
        from helpers_crypto.bitstampMy import bitstampHelper
        USERNAME, KEY, SECRET = decrypt('keysAndDecryption/bitstamp_0{}.bin'.format(PASSWORD_FILE)).split(" ")  # formerly bnk, bns, bfk, bfs
        WORKER = bitstampHelper(USERNAME, KEY, SECRET, ASSET_1, ASSET_2)
        WORKER.refresh_balances()
        logger.info('{} balance: {}, {} balance: {}'.format(ASSET_1.upper(), WORKER.balance_1, ASSET_2.upper(), WORKER.balance_2))
        # WORKER.place_orders(finalO)
    # elif EXCHANGE == 'binance':
    #     from helpers.binanceMy import binanceHelper
    # elif EXCHANGE == 'bitfinex':
    #     from helper_bitfinex import bitfinexHelper


class botCowen():
    """Docstring."""
    # NEKAM VKLJUCI program za racunanje pri katerih procentih(v odvisnosti od kolicine) se stvar se splaca:
    # zasluzek = (kolicina/2)*[moj procent]*(1-[trade fee (lahko sta razlicna buy, sell)]) > cena transakcij

    def __init__(self, EXCHANGE,
                 ASSET_1, ASSET_2, PERIOD,
                 LOWER_TREND, UPPER_TREND,
                 PASSWORD_FILE, DELETE_ORDERS=False):
        """Details:
        - PERIOD IN SECONDS [s]
        - _TREND is (k,n), defining a linear function y=kx+n, y is value, x is time."""
        logger.warning('888888888888888888888888888888 STARTING ANEW (INIT theBot) 888888888888888888888888888888')
        USERNAME, KEY, SECRET = decrypt(PASSWORD_FILE).split(" ")  # formerly bnk, bns, bfk, bfs
        # with open("/home/topkomp/localRepo/apiji.txt", "w+") as f:
        #     f.write("{} {} {} {}".format(bnk, bns, bfk, bfs))
        self.EXCHANGE = EXCHANGE(USERNAME, KEY, SECRET, LOWER_TREND, UPPER_TREND, ASSET_1, ASSET_2)
        self.ASSET_1 = ASSET_1
        self.ASSET_2 = ASSET_2
        self.PERIOD = PERIOD  # time between two consecutive loops in seconds [s]
        self.poorMode = False  # if some balance is too low to cover all 4 areas, we focus on only one exchange, MUST IMPLEMENT "diagonal" MECHANISM
        # ? self.delete_orders(all=True)
        if DELETE_ORDERS:
            self.EXCHANGE.delete_orders(all=True)

    def laufar(self):
        """Docstring."""
        count = 0
        exchange = self.EXCHANGE
        while True:
            logger.warning('{}. RUN:'.format(count+1)) if count % 51 == 0 else None
            count += 1
            # logger.info('{} OPEN ORDERS;\n{}'.format(exchange.__class__.__name__[:-6], pformat(openOrders)))
            try:
                withoutError = exchange.refresh_balances()
                logger.debug('laufar: refresh_balances() without error?:{}'.format(withoutError))
                exchange.refresh_orderBook()
                exchange.calculateOrders_cowen()
                # if not withoutError:
                #     exchange.delete_orders(exchange_1.firstOrders.keys())
                #     continue

                # if not exchange_1.refresh_orderBook():
                #     exchange_2.delete_orders(exchange_2.firstOrders.keys())
                # if not exchange_2.refresh_orderBook():
                #     exchange_1.delete_orders(exchange_1.firstOrders.keys())

                # if not exchange_1.refresh_openOrders():
                #     exchange_1.delete_orders(exchange_1.firstOrders.keys())
                # if not exchange_2.refresh_openOrders():
                #     exchange_2.delete_orders(exchange_2.firstOrders.keys())

                # if self.poorMode:
                #     if self.CHOSEN == 'EXCHANGE_1':  # Error in withoutError below means, that the other orderbook was empty
                #         self.poorMode, withoutError_1 = exchange_1.calculate_firstOrders(exchange_2.orderBook, exchange_2.balance_1, exchange_2.balance_2, self.poorMode)
                #     else:
                #         self.poorMode, withoutError_2 = exchange_2.calculate_firstOrders(exchange_1.orderBook, exchange_1.balance_1, exchange_1.balance_2, self.poorMode)
                # else:
                #     self.poorMode, withoutError_1 = exchange_1.calculate_firstOrders(exchange_2.orderBook, exchange_2.balance_1, exchange_2.balance_2, self.poorMode)
                #     self.poorMode, withoutError_2 = exchange_2.calculate_firstOrders(exchange_1.orderBook, exchange_1.balance_1, exchange_1.balance_2, self.poorMode)
                # if not withoutError_1:
                #     exchange_1.delete_orders(exchange_1.firstOrders.keys())
                # if not withoutError_2:
                #     exchange_2.delete_orders(exchange_2.firstOrders.keys())

                # exchange_1.loop_firstOrders()
                # exchange_2.loop_firstOrders()
                # if exchange_1.finalOrdersToBe or exchange_2.finalOrdersToBe:
                #     # DELETE THIS if-section SOME TIME IN THE FUTURE
                #     logger.error('WE HAVE FINAL ORDERS TO BE!')
                #     if exchange_1.finalOrdersToBe:
                #         logger.error('exchange_1.finalOrdersToBe:\n{}'.format(pformat(exchange_1.finalOrdersToBe)))
                #     else:
                #         logger.error('exchange_2.finalOrdersToBe:\n{}'.format(pformat(exchange_2.finalOrdersToBe)))

                # exchange_1.merge_calculatedFirst()
                # exchange_2.merge_calculatedFirst()

                # withoutError_1 = exchange_1.place_orders([], exchange_2.orderBook)
                # withoutError_2 = exchange_2.place_orders([], exchange_1.orderBook)
                # # withoutError_1 = exchange_1.place_orders(exchange_2.finalOrdersToBe, exchange_2.orderBook)
                # # withoutError_2 = exchange_2.place_orders(exchange_1.finalOrdersToBe, exchange_1.orderBook)
                # # exchange_1.finalOrdersToBe = []
                # # exchange_2.finalOrdersToBe = []
                # if not withoutError_1 or not withoutError_2:
                #     for exchange in [exchange_1, exchange_2]:
                #         exchange.delete_orders(exchange.firstOrders.keys())
                #     # self.brisi_vse()
                #     logger.critical(' => REVISE .place_orders()')
                #     try:
                #         import sys
                #         sys.exit(0)
                #     except SystemExit:
                #         import os
                #         os._exit(0)

                # for exchange in enumerate([self.EXCHANGE_1, self.EXCHANGE_2]):
                #     logger.info('{} calculated_firstOrders_:\n{}'.format(exchange[1].__class__.__name__[:-6], pformat(exec('calculated_firstOrders_{}'.format(exchange[0]+1)))))
                # if self.pm:
                #     logging.warning('# POOR MODE WAS ACTIVATED')
                # self.pm = False
                time.sleep(self.PERIOD)
            except KeyboardInterrupt:
                exchange.delete_orders(exchange.firstOrders.keys())
                # self.brisi_vse()
                logger.critical(' => CANCELED BY ME')
                try:
                    import sys
                    sys.exit(0)
                except SystemExit:
                    import os
                    os._exit(0)
            except Exception as e:
                logging.exception(e)
                exchange.delete_orders(exchange.firstOrders.keys())
                # self.brisi_vse()
                logger.critical(' => CANCELED BY ITSELF')
                try:
                    import sys
                    sys.exit(0)
                except SystemExit:
                    import os
                    os._exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--asset_1', help='e.g. btc, BTC, eth, ... Same for asset_2')
    parser.add_argument('--asset_2')
    parser.add_argument('--exchange', help='e.g. binance, bitstamp, bitfinex')
    parser.add_argument('--level_ch', default='info')
    parser.add_argument('--password_file', help='e.g. 1 for bitstamp_01.bin')  # default='keys/bitstamp_01.bin')
    parser.add_argument('--log_file', default='logs/PlacedOrders.log')
    parser.add_argument('--price', type=float)
    parser.add_argument('--quantity', type=float)
    args = parser.parse_args()

    logging_levels = {'debug': 10, 'info': 20, 'warning': 30, 'error': 40, 'critical': 50}

    fileHandler = logging.FileHandler(args.log_file)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging_levels[args.level_ch])
    consoleHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    logging.getLogger('BITSTAMP_LOGGER').setLevel(logging.DEBUG)
    logging.getLogger('BITSTAMP_LOGGER').addHandler(fileHandler)
    logging.getLogger('BITSTAMP_LOGGER').addHandler(consoleHandler)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.DEBUG)
    logging.getLogger('urllib3.connectionpool').addHandler(fileHandler)
    logging.getLogger('urllib3.connectionpool').addHandler(consoleHandler)

    placeOrder(args.exchange.lower(), args.password_file, 'btc', 'eth', 4, 4)
    # TheBot = botCowen(bitstampHelper,
    #                   args.asset_1,
    #                   args.asset_2,

    # TheBot.laufar()
