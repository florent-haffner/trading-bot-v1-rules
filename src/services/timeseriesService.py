import json

from src.helpers.dateHelper import set_datetime
from src.repository.missionRepository import getAllMissions
from src.repository.tradeEventRepository import getRecentEventByTypeAndAsset, insertTradeEvent, getAllEvents
from src.repository.tradeTransactionRepository import insertTransactionEvent, getTransactionById, updateTransactionById, \
    getTransactionByAsset, getLastDayTransactionByAsset


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


def calculateWinLossPerTransactions(transactions):
    total = []
    for transaction in transactions:
        typeOfTrade = ['buy', 'sell']
        transactionAmount = []
        for trade in typeOfTrade:
            try:
                field = transaction[trade]['fields']
                amountPerTransaction = field['quantity'] * field['price']
                transactionAmount.append(amountPerTransaction)

            except KeyError:
                pass

        if len(transactionAmount) == 1:
            current = -transactionAmount[0]
            total.append(current)
        else:
            totalPetTransaction = -transactionAmount[0] + transactionAmount[1]
            total.append(totalPetTransaction)

    totalAmount = 0
    for amountPerTransaction in total:
        totalAmount = totalAmount + amountPerTransaction

    return len(transactions), totalAmount


def calculateWInLossPerMission():
    print('\n[CALCULATING WIN/LOSS]\n')
    missions = list(getAllMissions())
    for mission in missions:
        for asset in mission['context']['assets']:
            print('\n[', asset, '] -> Calculating win/loss pet asset')
            transactionFromAsset = list(getTransactionByAsset(asset))
            lengthTransaction, amount = calculateWinLossPerTransactions(transactionFromAsset)
            print('Lgt transaction', lengthTransaction, 'amount', amount)


def getTransactionPerDayAsset(asset):
    return getLastDayTransactionByAsset(asset)


def analysingRecentTrades():
    events = getAllEvents()
    print(events.keys(), '\n')
    types = list(events.keys())
    for n in range(len(types)):
        eventType = types[n][1]['typeOfTrade']
        # print(eventType, list(events[list(events.keys())[n]]))
        print('\n[', eventType.upper(), ']')
        for event in list(events[list(events.keys())[n]]):
            print(json.dumps(event, indent=2))


if __name__ == '__main__':
    calculateWInLossPerMission()
    # analysingRecentTrades()

    # transactionsPerDay = list(getTransactionPerDayAsset('GRT'))
    # print('\ntransactionPerDay', transactionsPerDay)
