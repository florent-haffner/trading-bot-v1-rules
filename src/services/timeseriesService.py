from src.repository.tradeEventRepository import getRecentEventByTypeAndAsset, insertTradeEvent
from src.repository.tradeTransactionRepository import insertTransactionEvent, getTransactionById


def getLastEventByTypeAndAsset(asset, typeOfTrade):
    result = getRecentEventByTypeAndAsset(asset, typeOfTrade)
    for item in result:
        for n in item:
            if not n['acknowledge']:
                return n


def generateDTO(type_of_trade, volume_to_buy, df, maximum_index, asset, interval, date, transactionId):
    return {
        'measurement': 'tradeEvent',
        'time': date,
        'tags': {
            'typeOfTrade': type_of_trade,
            'interval': interval
        },
        'fields': {
            'transactionId': transactionId,
            'asset': asset,
            'quantity': volume_to_buy,
            'price': df['close'][maximum_index],
            'acknowledge': False
        }
    }


def addTradeEvent(type_of_trade, volume_to_buy, df, maximum_index, asset, interval, date, transactionId):
    point = generateDTO(type_of_trade, volume_to_buy, df, maximum_index, asset, interval, date, transactionId)
    if not transactionId:
        transactionId = insertTransactionEvent(type_of_trade, point)
    point['fields']['transactionId'] = str(transactionId)
    insertTradeEvent([point])


def getTransaction(id):
    return getTransactionById(id)
