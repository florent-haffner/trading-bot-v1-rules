from datetime import datetime

from src.helpers.dateHelper import DATE_UTC_TZ_STR
from src.data.tradeEventUtils import getRecentEventByTypeAndAsset, insertTradeEvent
from src.data.transactionMongoUtils import insertTransactionEvent, getTransactionById, \
    updateTransactionById, getLastDayCompleteTransactionByAsset, get_all_transactions_since_midnight_by_asset
from src.services.krakenTradeService import getLastPrice


def getLastTradeEventByTypeAndAsset(asset, typeOfTrade):
    print('Get las event by type', typeOfTrade, 'and asset:', asset)
    result = getRecentEventByTypeAndAsset(asset, typeOfTrade)
    most_recent = None
    for item in result:
        if not most_recent:
            most_recent = item
        if most_recent:
            if item['time'] > most_recent['time']:
                most_recent = item
    return most_recent


def generateTradeEventDTO(type_of_trade, volume_to_buy, asset, interval, price):
    return {
        'time': datetime.strftime(datetime.now(), DATE_UTC_TZ_STR),
        'measurement': 'tradeEvent',
        'tags': {
            'typeOfTrade': type_of_trade,
            'interval': interval
        },
        'fields': {
            'asset': asset,
            'quantity': volume_to_buy,
            'price': price
        }
    }


def addTradeEvent(type_of_trade, volume_to_buy, asset, interval, currency, transaction_id):
    success = False
    price = float(getLastPrice(asset, currency))
    point = generateTradeEventDTO(type_of_trade=type_of_trade, volume_to_buy=volume_to_buy,
                                  asset=asset, interval=interval, price=price)

    if not transaction_id:
        transaction_id = insertTransactionEvent(type_of_trade, point)
    point['fields']['transactionId'] = str(transaction_id)

    if type_of_trade == 'buy':
        # Adding new tradeEvent on InfluxDB
        del point['time']
        insertTradeEvent([point])
        success = True

    # Upgrading previous transaction on MongoDB
    if type_of_trade == 'sell':
        print('Updating', transaction_id, 'to complete transaction')
        result = updateTransaction(id=transaction_id,
                                   key=type_of_trade,
                                   data=point)
        if result:
            del point['time']
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


def getAllUnclosedTransactionSinceMidnightByAsset(asset):
    to_return: list = []
    results: list = get_all_transactions_since_midnight_by_asset(asset)
    for item in results:
        item_keys_length = len(list(item.keys()))
        if item_keys_length < 3:
            to_return.append(item)
    return to_return


def getTransactionPerDayAsset(asset):
    return getLastDayCompleteTransactionByAsset(asset)


if __name__ == '__main__':
    getAllUnclosedTransactionSinceMidnightByAsset('GRT')
