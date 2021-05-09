from datetime import datetime

from src.helpers.dateHelper import DATE_UTC_TZ_STR
from src.helpers.params import MAXIMUM_FEES
from src.repository.missionRepository import getAllMissions
from src.repository.tradeEventRepository import getRecentEventByTypeAndAsset, insertTradeEvent, getAllEvents
from src.repository.tradeTransactionRepository import insertTransactionEvent, getTransactionById, updateTransactionById, \
    getTransactionsByAsset, getLastDayTransactionByAsset
from src.services.krakenTradeService import getLastPrice


def getLastEventByTypeAndAsset(asset, typeOfTrade):
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


def generateDTO(type_of_trade, volume_to_buy, asset, interval, price):
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
    point = generateDTO(type_of_trade=type_of_trade, volume_to_buy=volume_to_buy,
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


def getTransactionPerDayAsset(asset):
    return getLastDayTransactionByAsset(asset)


# TODO -> not sure this is still usefull
"""
def analysingRecentTrades():
    result = {
        'buy': [],
        'sell': []
    }
    events = getAllEvents()
    for event in events:
        trade = event['typeOfTrade']
        if trade == 'buy':
            result['buy'].append(event)
        else:
            result['sell'].append(event)
    print('Nbr buy', len(result['buy']))
    print('Nbr sell', len(result['sell']))
"""
