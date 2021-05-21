from src.data.transactionMongoUtils import getTransactionById, updateTransactionById, \
    get_all_transactions_since_midnight_by_asset, getLastDayCompleteTransactionByAsset


def getTransaction(id):
    return getTransactionById(id)


def updateTransaction(id, key, data):
    document = getTransaction(id)
    try:
        if document['sell']:
            print('Document', id, 'already has been updated. Abort operation.')
            return False
    except KeyError:
        return updateTransactionById(id=id, key=key, updateTransaction=data)


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
