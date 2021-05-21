from pymongo import MongoClient

from src.helpers.params import __ENVIRONMENT
from src.secret.SECRET_CONSTANT import __MONGO_HOST, __MONGO_USER, __MONGO_PASSWORD, __MONGO_URI, __MONGO_DB

__MONGO_CLIENT = None

if __MONGO_URI:
    __MONGO_CLIENT = MongoClient(__MONGO_URI)
else:
    __MONGO_CLIENT = MongoClient(__MONGO_HOST, username=__MONGO_USER, password=__MONGO_PASSWORD)

db_name = __MONGO_DB + '_' + __ENVIRONMENT
db = __MONGO_CLIENT[db_name]
collection = db['mission']


def createMission(data):
    print('[MONGODB] - [NEW MISSION] ->', data)
    collection.insert_one(data)


def getAllMissions():
    print('[MONGODB] - [GET ALL MISSIONS]')
    return collection.find({})


def updateMission(id, updatedMission):
    print('[MONGODB] - [UPDATE MISSION] ->', updatedMission)
    query = dict(_id=id)
    values = {"$set": {"context": updatedMission}}

    collection.update_one(query, values)
    print('Updated', updatedMission)


def cleanMission():
    print('[MONGODB] - [REMOVING ALL MISSIONS]')
    collection.delete_many({})
    print('Done. Current list of missions:', list(collection.find({})))


if __name__ == '__main__':
    missions = list(getAllMissions())
    if not missions:
        missionData = {
            "context": {
                "interval": 1,
                "interval_unit": 'm',
                "assets": [
                    "GRT", "LINK", "ALGO"
                ]
            }
        }
        createMission(missionData)
        missions = list(getAllMissions())

    print(missions)

    missionId = missions[0]['_id']
    missionData = {
        "interval": 5,
        "interval_unit": 'm',
        "assets": [
            "GRT", "LINK", "ALGO"
        ]
    }
    updateMission(missionId, missionData)

    print(list(getAllMissions()))