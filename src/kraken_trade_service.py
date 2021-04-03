import krakenex
from datetime import datetime


class TradeToKrakenError(Exception): pass


API = krakenex.API()
API.load_key('../kraken.key')

"""
:param asset -> the currency, ex : BTC, ETH, GRT
"""


def getCurrentBalance(asset):
    try:
        return API.query_private('TradeBalance', {'asset': asset})
    except Exception as err:
        raise err


"""
:param asset -> the currency, ex : BTC, ETH, GRT
"""


def createNewOrder(asset, type, quantity):
    try:
        return API.query_private(
            'AddOrder', {
                'pair': asset,
                'type': type,
                'ordertype': 'market',
                'oflags': 'fciq',
                'volume': str(quantity),
                'starttm': str(datetime.timestamp(datetime.utcnow()))
            })
    except Exception as err:
        raise err


if __name__ == "__main__":
    balance = getCurrentBalance('ETH')
    print(balance)

    orderBuy = createNewOrder('ETHEUR', 'buy', 0.01)
    print(orderBuy)
    orderSell = createNewOrder('ETHEUR', 'sell', 0.01)
    print(orderSell)
