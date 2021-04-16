from pymongo import MongoClient

from src.secret.CONSTANT import __MONGO_HOST, __MONGO_USER, __MONGO_PASSWORD, __MONGO_URI

__MONGO_CLIENT = None

if __MONGO_URI:
    __MONGO_CLIENT = MongoClient(__MONGO_URI)
else:
    __MONGO_CLIENT = MongoClient(__MONGO_HOST, username=__MONGO_USER, password=__MONGO_PASSWORD)


db = __MONGO_CLIENT.tradingBot
collection = db.mission


def createMission(data):
    print('[MONGODB] - [NEW MISSION] ->', data)
    collection.insert_one(data)


def getAllMissions():
    print('[MONGODB] - [GET ALL MISSIONS]')
    return db.mission.find({})


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
    missionData = {
        "context": {
            "interval": 5,
            "assets": [
                "ETH"
            ]
        }
    }

    missions = list(getAllMissions())
    if not missions:
        createMission(missionData)
        missions = list(getAllMissions())
    print(missions)

    missionId = missions[0]['_id']
    missionData = {
        "interval": 5,
        "assets": [
            "GRT", "LINK", "ALGO"
        ]
    }
    updateMission(missionId, missionData)

    print(list(getAllMissions()))
    cleanMission()
