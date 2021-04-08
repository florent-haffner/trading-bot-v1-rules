from datetime import datetime

from timeseries_repository import getRecentEventByTypeAndAsset


def getLastEventByTypeAndAsset(asset, typeOfTrade):
    result = getRecentEventByTypeAndAsset(asset, typeOfTrade)
    for item in result:
        for n in item:
            if not n['acknowledge']:
                return n


def generateDTO(type_of_trade, volume_to_buy, df, maximum_index):
    return [
        {
            'measurement': 'tradeEvent',
            'time': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'tags': {
                'typeOfTrade': type_of_trade,
            },
            'fields': {
                'quantity': volume_to_buy,
                'price': df['close'][maximum_index],
                'acknowledge': False
            }
        }
    ]

def addEvent(type_of_trade, volume_to_buy, df, maximum_index):
    DTO = generateDTO(type_of_trade, volume_to_buy, df, maximum_index)
    print('save this')