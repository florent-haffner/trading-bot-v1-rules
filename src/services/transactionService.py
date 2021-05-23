from src.data.transactionMongoUtils import get_transaction_by_id, update_transaction_by_id, \
    get_all_transactions_since_last_week_by_asset, get_complete_transaction_from_last_day_by_asset


def getTransaction(id):
    return get_transaction_by_id(id)


def updateToCompleteTransaction(id, key, points):
    document = getTransaction(id)
    try:
        if document['sell']:
            print('Document', id, 'already has been updated. Abort operation.')
            return False
    except KeyError:
        update_transaction_by_id(_id=id, key=key, value=points)
        update_transaction_by_id(_id=id, key='forced_closed', value=False)
        return


def getAllUnclosedTransactionSinceMidnightByAsset(asset):
    to_return: list = []
    results: list = get_all_transactions_since_last_week_by_asset(asset)
    for item in results:
        item_keys_length = len(list(item.keys()))
        if item_keys_length < 3:
            to_return.append(item)
    return to_return


def get_complete_transaction_from_last_hours_per_asset(asset):
    return get_complete_transaction_from_last_day_by_asset(asset)


def getTransactionPerDayAsset(asset):
    return get_complete_transaction_from_last_day_by_asset(asset)


if __name__ == '__main__':
    res = getAllUnclosedTransactionSinceMidnightByAsset('ALGO')
    print(res[0]['buy']['time'])
    res = getAllUnclosedTransactionSinceMidnightByAsset('LINK')
    print(res[0]['buy']['time'])
    res = getAllUnclosedTransactionSinceMidnightByAsset('GRT')
    print(res[0]['buy']['time'])
