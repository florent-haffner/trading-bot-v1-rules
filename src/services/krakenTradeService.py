import os
from datetime import datetime
from typing import Dict, Any

import krakenex


class TradeToKrakenError(Exception):
    super(Exception)


API = krakenex.API()
current_file_absolute_path = os.path.dirname(os.path.realpath(__file__))
API.load_key(current_file_absolute_path + '/../' + 'secret/kraken.key')


def getTradeBalance(asset: str) -> Dict[str, Any]:
    """
    :param asset -> BTC, ETH, GRT
    """
    try:
        return API.query_private('TradeBalance', {'asset': asset})
    except Exception as err:
        raise err


def getAccountBalance() -> Dict[str, Any]:
    try:
        return API.query_private('Balance')
    except Exception as err:
        raise err


def createNewOrder(asset: str, type: str, quantity: float): # TODO : check the return type -> if possible to get the price bought
    """
    :param asset ->  BTC, ETH, GRT
    :param type ->  buy, sell
    :param quantity -> calculated based on wallet balance
    """
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


def getLastPrice(asset: str, currency: str) -> float:
    """
    :param asset -> BTC, ETH, GRT
    :param currency -> EU
    """
    try:
        combo = str(asset + currency).upper()
        result = API.query_public(
            'Ticker', {
                'pair': combo,
            })
        if result:
            output = result['result'][combo]['a'][0]
            return float(output)
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
