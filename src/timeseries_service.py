from timeseries_repository import getRecentEventByTypeAndAsset


def getLastEventByTypeAndAsset(asset, typeOfTrade):
    result = getRecentEventByTypeAndAsset(asset, typeOfTrade)
    for item in result:
        for n in item:
            if not n['acknowledge']:
                return n
