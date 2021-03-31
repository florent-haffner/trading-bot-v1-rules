import krakenex


class TradeToKrakenError(Exception): pass


"""
:param asset -> the pair of currency, ex : BTCEUR, ETHEUR, ALGOUSD
:param interval -> data interval in minutes (1, 5, 10, 60, 120, 360, 1440)
"""
def getCurrentBalance(asset):
    try:
        k = krakenex.API()
        k.load_key('../kraken_api_key.txt')
        return k.query_private('TradeBalance', {'asset': asset})

    except Exception as err:
        raise err


if __name__ == "__main__":
    balance = getCurrentBalance('ETH')
    print(balance)