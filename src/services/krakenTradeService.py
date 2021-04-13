import os
from datetime import datetime

import krakenex


class TradeToKrakenError(Exception): pass


API = krakenex.API()
current_file_absolute_path = os.path.dirname(os.path.realpath(__file__))
API.load_key(current_file_absolute_path + '/../' + 'secret/kraken.key')

"""
:param asset -> the currency, ex : BTC, ETH, GRT
"""
def getTradeBalance(asset):
    try:
        return API.query_private('TradeBalance', {'asset': asset})
    except Exception as err:
        raise err

"""
:param asset -> the currency, ex : BTC, ETH, GRT
"""

def getAccountBalance():
    try:
        return API.query_private('Balance')
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
    # asset = 'GRT'
    # curreny = 'EUR'
    # volumeToBuy = 20
    #
    # tradeBalance = getTradeBalance(asset)
    # print(tradeBalance)
    #
    # orderBuy = createNewOrder(asset + curreny, 'buy', volumeToBuy)
    # print(orderBuy)
    #
    # tradeBalance = getTradeBalance(asset)
    # print(tradeBalance)
    #
    # orderSell = createNewOrder(asset + curreny, 'sell', volumeToBuy)
    # print(orderSell)
    #
    # tradeBalance = getTradeBalance(asset)
    # print(tradeBalance)

    accountBalance = getAccountBalance()
    print(accountBalance)
