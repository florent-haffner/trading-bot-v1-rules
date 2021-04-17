from datetime import datetime, timedelta

from bson import ObjectId
from pymongo import MongoClient

from src.helpers.CONSTANT import DATE_STR
from src.secret.SECRET_CONSTANT import __MONGO_HOST, __MONGO_USER, __MONGO_PASSWORD, __MONGO_URI

__MONGO_CLIENT = None

if __MONGO_URI:
    __MONGO_CLIENT = MongoClient(__MONGO_URI)
else:
    __MONGO_CLIENT = MongoClient(__MONGO_HOST, username=__MONGO_USER, password=__MONGO_PASSWORD)


db = __MONGO_CLIENT.tradingBot
collection = db.tradeTransaction


def getTransactionById(id):
    print('[MONGODB] - [GET TRANSACTIONS BY ID] ->', id)
    return collection.find_one({"_id": ObjectId(id)})

def insertTransactionEvent(key, data):
    print('[MONGODB] - [NEW TRANSACTION] ->', data)
    transactionId = collection.insert_one({key: data})
    return transactionId.inserted_id


def getAllTransaction():
    print('[MONGODB] - [GET ALL TRANSACTIONS]')
    return collection.find({})


def updateTransactionById(id, key, updateTransaction):
    print('[MONGODB] - [UPDATING TRANSACTION] ->', id)
    values = {"$set": {key: updateTransaction}}
    return collection.update_one(
        filter=dict({'_id': ObjectId(id)}),
        update=values,
        upsert=False)


def cleanTransaction():
    print('[MONGODB] - [REMOVING ALL TRANSACTION]')
    collection.delete_many({})
    print('Done. Current list of TRANSACTION:', list(collection.find({})))


def initEnvironment():
    timeseries_buy = {
        'measurement': 'tradeEvent',
        'time': datetime.now().strftime(DATE_STR),
        'tags': {
            'typeOfTrade': 'buy',
            'interval': '5'
        },
        'fields': {
            'asset': 'ETH',
            'quantity': 200,
            'price': 200,
            'acknowledge': False
        }
    }

    transactions = list(getAllTransaction())
    if not transactions:
        insertTransactionEvent(
            key=timeseries_buy['tags']['typeOfTrade'],
            data=timeseries_buy)
        transactions = list(getAllTransaction())
    print(transactions)

    transactionId = transactions[0]['_id']
    timeseries_sell = {
        'measurement': 'tradeEvent',
        'time': datetime.now().strftime(DATE_STR),
        'tags': {
            'typeOfTrade': 'sell',
            'interval': '5'
        },
        'fields': {
            'asset': 'ETH',
            'quantity': 200,
            'price': 200,
            'acknowledge': False
        }
    }
    updateTransactionById(id=transactionId,
                          key=timeseries_sell['tags']['typeOfTrade'],
                          updateTransaction=timeseries_sell)


def getTransactionByAsset(asset):
    return collection.find({
        'buy.fields.asset': asset,
    })


def getLastDayTransactionByAsset(asset):
    previousDay = datetime.now() - timedelta(days=1)
    return collection.find({
        'buy.fields.asset': asset,
        'buy.time': {'$gte': previousDay.strftime(DATE_STR)},
    })


if __name__ == '__main__':
    # initEnvironment()

    transactions = list(getAllTransaction())
    print('nbr transaction', len(transactions))
    for transaction in transactions:
        print(transaction)

    # cleanTransaction()
