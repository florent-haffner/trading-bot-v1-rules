import os
from datetime import datetime
from time import sleep

import krakenex


class KrakenTradeError(Exception):
    super(Exception)


API = krakenex.API()
current_file_absolute_path = os.path.dirname(os.path.realpath(__file__))
API.load_key(current_file_absolute_path + '/../' + 'secret/kraken.key')


def get_trade_balance(asset: str) -> dict:
    """
    :param asset -> BTC, ETH, GRT
    :return: a dictionary of the account balance based using the asset price and stuff
    """
    try:
        return API.query_private('TradeBalance', {'asset': asset})
    except Exception as err:
        raise err


def get_account_balance() -> dict:
    """
    :return: a JSON object of the current balance of the kraken account
    """
    try:
        return API.query_private('Balance')
    except Exception as err:
        raise err


def create_new_order(pair: str, type: str, quantity: float) -> dict:
    """
    :param pair ->  BTC, ETH, GRT
    :param type ->  buy, sell
    :param quantity -> calculated based on wallet balance
    :return: a JSON object of the trade transaction with order details and "txid"
    """
    print('[KRAKEN TRADE PLATFORM]')
    print('New trade on Kraken', 'type:', type, 'pair:', pair, 'quantity:', quantity)
    print('-----------------------')
    try:
        return API.query_private(
            'AddOrder', {
                'pair': pair,
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
        results = API.query_public(
            'Ticker', {
                'pair': str(asset + currency).upper(),
            })
        if results:
            result_asset_key = list(results['result'].keys())[0]
            output_price = results['result'][result_asset_key]['a'][0]
            return float(output_price)
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
    accountBalance = get_account_balance()
    print('account balance', accountBalance)
    tradeBalance = get_trade_balance(asset)
    print('with', asset, tradeBalance)

    trade_type = 'sell'
    order_sell = create_new_order(asset + currency, trade_type, volume_to_buy)
    price = get_last_price(asset, currency)
    print(trade_type, order_sell, '@', price)
    tradeBalance = get_trade_balance(asset)
    print('trade balance', tradeBalance)
    accountBalance = get_account_balance()
    print('account balance', accountBalance)
