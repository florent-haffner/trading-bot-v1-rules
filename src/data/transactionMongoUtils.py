from datetime import datetime, timedelta

from bson import ObjectId
from pymongo import MongoClient

from src.helpers.dateHelper import DATE_STR
from src.helpers.params import __ENVIRONMENT
from src.secret.SECRET_CONSTANT import __MONGO_URI, __MONGO_DB

__MONGO_CLIENT = MongoClient(__MONGO_URI)

db_name = __MONGO_DB + '_' + __ENVIRONMENT
db = __MONGO_CLIENT[db_name]
collection = db['tradeTransaction']
__MODEL_VERSION: float = 1.0


def getTransactionById(id):
    print('[MONGODB] - [GET TRANSACTIONS BY ID] ->', id)
    return collection.find_one({"_id": ObjectId(id)})


def insertTransactionEvent(key, data):
    print('[MONGODB] - [NEW TRANSACTION] ->', data)
    data['time'] = datetime.now().strftime(DATE_STR)
    data['version'] = __MODEL_VERSION
    transactionId = collection.insert_one({key: data})
    return transactionId.inserted_id


def getAllTransaction():
    print('[MONGODB] - [GET ALL TRANSACTIONS]')
    return collection.find({})


def updateTransactionById(id, key, value):
    print('[MONGODB] - [UPDATING TRANSACTION] ->', id)
    values = {"$set": {key: value}}
    return collection.update_one(
        filter=dict({'_id': ObjectId(id)}),
        update=values,
        upsert=False
    )


def cleanTransaction():
    print('[MONGODB] - [REMOVING ALL TRANSACTION]')
    collection.delete_many({})
    print('Done. Current list of TRANSACTION:', list(collection.find({})))


# TODO -> remove this if not needed
"""
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
                          value=timeseries_sell)
"""

def get_all_transactions_since_midnight_by_asset(asset):
    previousDayFromMidnight = datetime.combine(datetime.today() - timedelta(days=1), datetime.min.time())
    return collection.find({
        'buy.fields.asset': asset,
        'buy.time': {'$gte': previousDayFromMidnight.strftime(DATE_STR)},
    })


def getTransactionsByAsset(asset):
    return collection.find({
        'buy.fields.asset': asset,
    })


def getLastDayCompleteTransactionByAsset(asset):
    previousDayFromMidnight = datetime.combine(datetime.today() - timedelta(days=1), datetime.min.time())
    thisDayAtMidgnight = datetime.combine(datetime.today(), datetime.min.time())

    return collection.find({
        'buy.fields.asset': asset,
        'buy.time': {'$gte': previousDayFromMidnight.strftime(DATE_STR)},
        'sell.time': {'$lte': thisDayAtMidgnight.strftime(DATE_STR)},
    })


if __name__ == '__main__':
    # initEnvironment()

    transactions = list(getAllTransaction())
    # print('nbr transaction', len(transactions))

    for transaction in transactions:
        id = transaction['_id']
        # print(id, type(id))
        updateTransactionById(id, 'version', __MODEL_VERSION)

    transactions = list(getAllTransaction())
    for transaction in transactions:
        print(transaction.keys())

    # cleanTransaction()
