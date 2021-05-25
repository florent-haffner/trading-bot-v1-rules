from datetime import datetime

from pymongo import MongoClient

from src.helpers.dateHelper import DATE_STR
from src.helpers.params import __ENVIRONMENT
from src.secret.SECRET_CONSTANT import __MONGO_HOST, __MONGO_USER, __MONGO_PASSWORD, __MONGO_URI, __MONGO_DB

__MONGO_CLIENT = None

if __MONGO_URI:
    __MONGO_CLIENT = MongoClient(__MONGO_URI)
else:
    __MONGO_CLIENT = MongoClient(__MONGO_HOST, username=__MONGO_USER, password=__MONGO_PASSWORD)

db_name = __MONGO_DB + '_' + __ENVIRONMENT
db = __MONGO_CLIENT[db_name]
collection = db['wallet_evolution']

__VERSION = 1.0


def create_wallet_evolution(data: dict):
    print('[MONGODB] - [NEW MISSION] ->', data)
    return collection.insert_one(data)


def get_all_wallet_evolution():
    print('[MONGODB] - [GET ALL MISSIONS]')
    return collection.find({})


def clean_wallet_evolution():
    """
    [MONGODB] - [REMOVING ALL MISSIONS]
    :return: None
    """
    collection.delete_many({})
    print('Done. Current list of missions:', list(collection.find({})))


def generate_wallet_evolution_dto(event: dict, account_balance: float):
    return {
        "time": datetime.now().strftime(DATE_STR),
        "version": __VERSION,
        "event": event,
        "account_balance": account_balance
    }
