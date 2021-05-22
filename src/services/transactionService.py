from src.data.transactionMongoUtils import getTransactionById, updateTransactionById, \
    get_all_transactions_since_midnight_by_asset, getLastDayCompleteTransactionByAsset


def getTransaction(id):
    return getTransactionById(id)


def updateToCompleteTransaction(id, key, points):
    document = getTransaction(id)
    try:
        if document['sell']:
            print('Document', id, 'already has been updated. Abort operation.')
            return False
    except KeyError:
        updateTransactionById(id=id, key=key, value=points)
        updateTransactionById(id=id, key='forced_closed', value=False)
        return


def getAllUnclosedTransactionSinceMidnightByAsset(asset):
    to_return: list = []
    results: list = get_all_transactions_since_midnight_by_asset(asset)
    for item in results:
        item_keys_length = len(list(item.keys()))
        if item_keys_length < 3:
            to_return.append(item)
    return to_return


def getTransactionPerDayAsset(asset):
    return getLastDayCompleteTransactionByAsset(asset)


if __name__ == '__main__':
    res = getAllUnclosedTransactionSinceMidnightByAsset('ALGO')
    print(res[0]['buy']['time'])
    res = getAllUnclosedTransactionSinceMidnightByAsset('LINK')
    print(res[0]['buy']['time'])
    res = getAllUnclosedTransactionSinceMidnightByAsset('GRT')
    print(res[0]['buy']['time'])
