from datetime import datetime

from src.repository.tradeEventRepository import getRecentEventByTypeAndAsset, insertTradeEvent
from src.repository.tradeTransactionRepository import insertTransactionEvent, getTransactionById, updateTransactionById


def set_datetime(datetime_str):
    return datetime.strptime(datetime_str[:-1], '%Y-%m-%dT%H:%M:%S')


def getLastEventByTypeAndAsset(asset, typeOfTrade):
    result = getRecentEventByTypeAndAsset(asset, typeOfTrade)
    for items in result:
        most_recent = None
        for item in items:
            if not most_recent:
                most_recent = item
            if most_recent:
                most_recent_time = set_datetime(most_recent['time'])
                last_time = set_datetime(item['time'])
                if last_time > most_recent_time:
                    most_recent = item
        return most_recent


def generateDTO(type_of_trade, volume_to_buy, df, maximum_index, asset, interval, date):
    return {
        'measurement': 'tradeEvent',
        'time': date,
        'tags': {
            'typeOfTrade': type_of_trade,
            'interval': interval
        },
        'fields': {
            'asset': asset,
            'quantity': volume_to_buy,
            'price': df['close'][maximum_index]
        }
    }


def addTradeEvent(type_of_trade, volume_to_buy, df, maximum_index, asset, interval, date, transactionId):
    success = False
    point = generateDTO(type_of_trade, volume_to_buy, df, maximum_index, asset, interval, date)

    if not transactionId:
        transactionId = insertTransactionEvent(type_of_trade, point)
        print(transactionId)
    point['fields']['transactionId'] = str(transactionId)

    if type_of_trade == 'buy':
        # Adding new tradeEvent on InfluxDB
        insertTradeEvent([point])
        success = True

    # Upgrading previous transaction on MongoDB
    if type_of_trade == 'sell':
        print('Updating', transactionId, 'to complete transaction')
        result = updateTransaction(id=transactionId,
                                   key=type_of_trade,
                                   data=point)
        if result:
            insertTradeEvent([point])
            success = True
    return success


def getTransaction(id):
    return getTransactionById(id)


def updateTransaction(id, key, data):
    document = getTransaction(id)
    try:
        if document['sell']:
            print('Document', id, 'already has been updated. Abort operation.')
            return False
    except KeyError:
        return updateTransactionById(id=id, key=key, updateTransaction=data)
