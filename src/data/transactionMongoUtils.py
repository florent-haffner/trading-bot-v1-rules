from datetime import datetime, timedelta

from bson import ObjectId
from pymongo import MongoClient

from src.helpers.dateHelper import DATE_STR
from src.helpers.params import __ENVIRONMENT
from src.secret.keys import __MONGO_URI, __MONGO_DB

__MONGO_CLIENT = MongoClient(__MONGO_URI)

db_name = __MONGO_DB + '_' + __ENVIRONMENT
db = __MONGO_CLIENT[db_name]
collection = db['trade_transactions']
__MODEL_VERSION: float = 1.0


def get_transaction_by_id(id: str):
    """
    [MONGODB] - [GET TRANSACTIONS BY ID] ->', id)
    :param id
    :return:
    """
    return collection.find_one({"_id": ObjectId(id)})


def get_all_transaction():
    """
    [MONGODB] - [GET ALL TRANSACTIONS]
    :param: None
    :return: mongodb cursor
    """
    return collection.find({})


def update_transaction_by_id(_id: str, key: str, value: object):
    """
    [MONGODB] - [UPDATING TRANSACTION]
    :param _id: str
    :param key: object key (time, buy, sell, version, forced_closed)
    :param value: the value to update
    :return:
    """
    values = {"$set": {key: value}}
    return collection.update_one(
        filter=dict({'_id': ObjectId(_id)}),
        update=values,
        upsert=False
    )


def clean_transaction():
    """
    [MONGODB] - [REMOVING ALL TRANSACTION]
    :return: None
    """
    collection.delete_many({})
    print('Done. Current list of TRANSACTION:', list(collection.find({})))


def get_all_transactions_since_midnight():
    """
    :return: None
    """
    last_week: datetime = datetime.combine(datetime.today() - timedelta(weeks=1), datetime.min.time())
    return collection.find({
        'buy.time': {'$gte': last_week.strftime(DATE_STR)},
    })


def get_all_transactions_since_last_week_by_asset(asset: str):
    """
    :param: asset to query
    :return: cursor with all transaction since midnight for a specific asset
    """
    previousDayFromMidnight: datetime = datetime.combine(datetime.today() - timedelta(days=1), datetime.min.time())
    return collection.find({
        'buy.fields.asset': asset,
        'buy.time': {'$gte': previousDayFromMidnight.strftime(DATE_STR)},
    })


def get_transactions_by_asset(asset: str):
    """
    :param: asset to query
    :return: all transaction for a specific asset
    """
    return collection.find({
        'buy.fields.asset': asset,
    })


def get_complete_transaction_from_the_last_24h_by_asset(asset: str):
    """
    :param: asset to query
    :return: all complete transaction the last 24 hours for a specific asset """
    now: datetime = datetime.now()
    twenty_four_hours_before: datetime = now - timedelta(days=1)
    return collection.find({
        'buy.fields.asset': asset,
        'buy.time': {'$gte': twenty_four_hours_before.strftime(DATE_STR)},
        'sell.time': {'$lte': now.strftime(DATE_STR)},
    })


def get_complete_transaction_from_last_day_by_asset(asset: str):
    """
    :param: asset to query
    :return: all complete transaction since midnight for a specific asset
    """
    previous_day_at_midnight: datetime = datetime.combine(datetime.today() - timedelta(days=1), datetime.min.time())
    this_day_at_midnight: datetime = datetime.combine(datetime.today(), datetime.min.time())
    return collection.find({
        'buy.fields.asset': asset,
        'buy.time': {'$gte': previous_day_at_midnight.strftime(DATE_STR)},
        'sell.time': {'$lte': this_day_at_midnight.strftime(DATE_STR)},
    })


def insert_transaction(data: dict):
    return collection.insert_one(data)


if __name__ == '__main__':
    # initEnvironment()

    transactions = list(get_all_transaction())
    print('nbr transaction', len(transactions))
    for transaction in transactions:
        print(transaction)

    # res = list(get_complete_transaction_from_the_last_24h_by_asset('ALGO'))
    # print('nbr transaction', len(res))

    # clean_transaction()
