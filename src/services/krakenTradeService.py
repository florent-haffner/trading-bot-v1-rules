import os
from datetime import datetime
from time import sleep
from typing import Dict, Any

import krakenex


class TradeToKrakenError(Exception):
    super(Exception)


API = krakenex.API()
current_file_absolute_path = os.path.dirname(os.path.realpath(__file__))
API.load_key(current_file_absolute_path + '/../' + 'secret/kraken.key')


def get_trade_balance(asset: str) -> Dict[str, Any]:
    """
    :param asset -> BTC, ETH, GRT
    :return: a dictionary of the account balance based using the asset price and stuff
    """
    try:
        return API.query_private('TradeBalance', {'asset': asset})
    except Exception as err:
        raise err


def get_account_balance() -> Dict[str, Any]:
    """
    :return: a JSON object of the current balance of the kraken account
    """
    try:
        return API.query_private('Balance')
    except Exception as err:
        raise err


def create_new_order(asset: str, type: str, quantity: float) -> Dict[str, Any]:
    """
    :param asset ->  BTC, ETH, GRT
    :param type ->  buy, sell
    :param quantity -> calculated based on wallet balance
    :return: a JSON object of the trade transaction with order details and "txid"
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


def get_last_price(asset: str, currency: str) -> float:
    """
    :param asset -> BTC, ETH, GRT
    :param currency -> EU
    :return: the last price in float
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
    asset = 'GRT'
    currency = 'EUR'
    volume_to_buy = 30

    accountBalance = get_account_balance()
    print('account balance', accountBalance)

    tradeBalance = get_trade_balance(asset)
    print('init', tradeBalance)

    trade_type = 'buy'
    order_buy = create_new_order(asset + currency, trade_type, volume_to_buy)
    price = get_last_price(asset, currency)
    print(trade_type, order_buy, '@', price)

    wait_time = 10
    print('Wait for', wait_time, 's')
    sleep(wait_time)

    tradeBalance = get_trade_balance(asset)
    print('with', asset, tradeBalance)

    trade_type = 'sell'
    order_sell = create_new_order(asset + currency, trade_type, volume_to_buy)
    price = get_last_price(asset, currency)
    print(trade_type, order_sell, '@', price)

    print('Wait for', wait_time, 's')
    sleep(wait_time)

    tradeBalance = get_trade_balance(asset)
    print('trade balance', tradeBalance)

    accountBalance = get_account_balance()
    print('account balance', accountBalance)
