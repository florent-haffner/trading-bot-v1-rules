from datetime import datetime

from src.repository.timeseriesRepository import getRecentEventByTypeAndAsset, addTradeEvent


def getLastEventByTypeAndAsset(asset, typeOfTrade):
    result = getRecentEventByTypeAndAsset(asset, typeOfTrade)
    for item in result:
        for n in item:
            if not n['acknowledge']:
                return n


def generateDTO(type_of_trade, volume_to_buy, df, maximum_index, asset, interval):
    return [
        {
            'measurement': 'tradeEvent',
            'time': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'tags': {
                'typeOfTrade': type_of_trade,
                'interval': interval
            },
            'fields': {
                'asset': asset,
                'quantity': volume_to_buy,
                'price': df['close'][maximum_index],
                'acknowledge': False
            }
        }
    ]


def addEvent(type_of_trade, volume_to_buy, df, maximum_index, asset, interval):
    point = generateDTO(type_of_trade, volume_to_buy, df, maximum_index, asset, interval)
    addTradeEvent(point)
