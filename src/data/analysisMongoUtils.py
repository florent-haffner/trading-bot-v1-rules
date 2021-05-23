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
collection = db['analysis']


def create_domain_object(data, type_of_analysis):
    return {
        "time": datetime.now().strftime(DATE_STR),
        "type": type_of_analysis,
        "analysis": data
    }


def insert_analysis(data):
    print('[MONGODB] - [NEW ANALYSIS] ->', data)
    collection.insert_one(data)


def get_all_analysis():
    print('[MONGODB] - [GET ALL ANALYSIS]')
    return collection.find({})


def clean_analysis():
    print('[MONGODB] - [REMOVING ALL ANALYSIS]')
    collection.delete_many({})
    print('Done. Current list of analysis:', list(collection.find({})))


if __name__ == '__main__':
    toStore = [
      {
        "asset": "GRT",
        "beginning_amount": 0,
        "nbr_transactions": 0,
        "result": 0,
        "percent": 0
      },
      {
        "asset": "LINK",
        "beginning_amount": 21.49,
        "nbr_transactions": 3,
        "result": 0.48,
        "percent": 2.23
      },
      {
        "asset": "ALGO",
        "beginning_amount": 21.52,
        "nbr_transactions": 16,
        "result": 0.932,
        "percent": 4.33
      },
      {
        "asset": "total",
        "beginning_amount": 43.01,
        "nbr_transactions": 19,
        "result": 3.283,
        "percent": 7.63
      }
    ]
    data = create_domain_object(toStore, 'daily')
    insert_analysis(data)
    print(list(get_all_analysis()))
