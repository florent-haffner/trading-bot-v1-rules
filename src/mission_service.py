from pymongo import MongoClient

from CONSTANT import __MONGO_HOST, __MONGO_USER, __MONGO_PASSWORD

__MONGO_CLIENT = MongoClient(__MONGO_HOST,
                             username=__MONGO_USER,
                             password=__MONGO_PASSWORD)

db = __MONGO_CLIENT.test_database
collection = db.mission


def createMission(data):
    print('[NEW MISSION] ->', data)
    collection.insert_one(data)


def getAllMissions():
    return db.mission.find({})


def updateMission(id, updatedMission):
    print('[UPDATE MISSION] ->', updatedMission)
    query = dict(_id=id)
    values = {"$set": {"context.assets": updatedMission}}

    collection.update_one(query, values)
    print('Updated', updatedMission)


def cleanMission():
    print('[REMOVING ALL MISSIONS]')
    collection.delete_many({})
    print('Done. Current list of missions:', list(collection.find({})))


if __name__ == '__main__':
    missionData = {"context": {
        "interval": 60,
        "assets": [
            {"asset": "GRT"}
        ]
    }}
    createMission(missionData)

    missions = list(getAllMissions())
    print(missions)

    missionId = missions[0]['_id']
    missionData = {"context": {
        "interval": 60,
        "assets": [
            {"asset": "GRT"},
            {"asset": "LINK"},
            {"asset": "ALGO"}
        ]
    }}
    updateMission(missionId, missionData)

    print(list(getAllMissions()))
    cleanMission()
