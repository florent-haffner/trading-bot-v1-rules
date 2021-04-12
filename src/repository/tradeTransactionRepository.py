from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient

from src.secret.CONSTANT import __MONGO_HOST, __MONGO_USER, __MONGO_PASSWORD, __MONGO_URI

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


def updateTransaction(id, key, updateTransaction):
    query = dict(_id=id)
    values = {"$set": { str(key): updateTransaction }}
    collection.update_one(query, values)
    print('[MONGODB] - [UPDATED TRANSACTION] ->', id)


def cleanTransaction():
    print('[MONGODB] - [REMOVING ALL TRANSACTION]')
    collection.delete_many({})
    print('Done. Current list of TRANSACTION:', list(collection.find({})))


if __name__ == '__main__':
    # timeseries_buy = {
    #     'measurement': 'tradeEvent',
    #     'time': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    #     'tags': {
    #         'typeOfTrade': 'buy',
    #         'interval': '5'
    #     },
    #     'fields': {
    #         'asset': 'ETH',
    #         'quantity': 200,
    #         'price': 200,
    #         'acknowledge': False
    #     }
    # }
    #
    # transactions = list(getAllTransaction())
    # if not transactions:
    #     insertTransactionEvent(
    #         key=timeseries_buy['tags']['typeOfTrade'],
    #         data=timeseries_buy)
    #     transactions = list(getAllTransaction())
    # print(transactions)
    #
    # transactionId = transactions[0]['_id']
    # timeseries_sell = {
    #     'measurement': 'tradeEvent',
    #     'time': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    #     'tags': {
    #         'typeOfTrade': 'sell',
    #         'interval': '5'
    #     },
    #     'fields': {
    #         'asset': 'ETH',
    #         'quantity': 200,
    #         'price': 200,
    #         'acknowledge': False
    #     }
    # }
    # updateTransaction(id=transactionId,
    #                   key=timeseries_sell['tags']['typeOfTrade'],
    #                   updateTransaction=timeseries_sell)

    print(list(getAllTransaction()))
    cleanTransaction()

    # transaction = getTransactionById(transactionId)
    # print(transaction)
