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


def create_domain_object(data: list, type_of_analysis: str):
    """
    :param data: the list of analysis
    :param type_of_analysis: daily/weekly
    :return: a dictionary to store on MongoDB
    """
    return {
        "time": datetime.now().strftime(DATE_STR),
        "type": type_of_analysis,
        "analysis": data
    }


def insert_analysis(data):
    """
    :param data: the analysis to store
    :return: cursor
    """
    collection.insert_one(data)


def get_all_analysis():
    """
    :return: all the analysis known
    """
    return collection.find({})


def clean_analysis():
    """
    Remove all the stored analysis
    :return: None
    """
    collection.delete_many({})
    print('Done. Current list of analysis:', list(collection.find({})))
