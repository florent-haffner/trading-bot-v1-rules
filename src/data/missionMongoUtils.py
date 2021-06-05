from pymongo import MongoClient

from src.helpers.params import __ENVIRONMENT
from src.secret.db_keys import __MONGO_HOST, __MONGO_USER, __MONGO_PASSWORD, __MONGO_URI, __MONGO_DB

__MONGO_CLIENT = None

if __MONGO_URI:
    __MONGO_CLIENT = MongoClient(__MONGO_URI)
else:
    __MONGO_CLIENT = MongoClient(__MONGO_HOST, username=__MONGO_USER, password=__MONGO_PASSWORD)

db_name = __MONGO_DB + '_' + __ENVIRONMENT
db = __MONGO_CLIENT[db_name]
collection = db['mission']

__VERSION = 1.0


def create_mission(data: dict):
    print('[MONGODB] - [NEW MISSION] ->', data)
    collection.insert_one(data)


def get_all_missions():
    print('[MONGODB] - [GET ALL MISSIONS]')
    return collection.find({})


def update_mission(id: str, data: dict):
    """
    :param id: identifier
    :param data: dictionary /w the knowledge
    :return: None
    """
    query = dict(_id=id)
    values = {"$set": {"context": data}}
    collection.update_one(query, values)
    print('Updated', id, 'with', data)


def cleanMission():
    """
    [MONGODB] - [REMOVING ALL MISSIONS]
    :return: None
    """
    collection.delete_many({})
    print('Done. Current list of missions:', list(collection.find({})))


if __name__ == '__main__':
    missions = list(get_all_missions())
    if not missions:
        missionData = {
            "version": __VERSION,
            "context": {
                "interval": 1,
                "interval_unit": 'm',
                "assets": [
                    "GRT", "LINK", "ALGO"
                ]
            }
        }
        create_mission(missionData)
        missions = list(get_all_missions())

    print(missions)

    missionId = missions[0]['_id']
    missionData = {
        "interval": 5,
        "interval_unit": 'm',
        "assets": [
            "GRT", "LINK", "ALGO"
        ]
    }
    update_mission(missionId, missionData)

    print(list(get_all_missions()))
