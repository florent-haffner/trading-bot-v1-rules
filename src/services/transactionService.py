from src.data.transactionMongoUtils import get_transaction_by_id, update_transaction_by_id, \
    get_complete_transaction_from_last_day_by_asset


def get_transaction(_id: str):
    """
    :param _id: string to query
    :return: MongoDB cursor
    """
    return get_transaction_by_id(_id)


def update_to_complete_transaction(_id: str, key: str, points: dict):
    """
    :param _id: string to query
    :param key: the key to help specify the query
    :param points: the dictionary to add
    :return: None or False
    """
    document = get_transaction(_id)
    try:
        if document['sell']:
            print('Document', _id, 'already has been updated. Abort operation.')
            return False
    except KeyError:
        update_transaction_by_id(_id=_id, key=key, value=points)
        update_transaction_by_id(_id=_id, key='forced_closed', value=False)
        return


# TODO -> not sure it's still useful
"""
def get_all_unclosed_transaction_since_midnight_by_asset(asset):
    to_return: list = []
    results: list = get_all_transactions_since_last_week_by_asset(asset)
    for item in results:
        item_keys_length = len(list(item.keys()))
        if item_keys_length < 3:
            to_return.append(item)
    return to_return

def get_complete_transaction_from_last_hours_per_asset(asset):
    return get_complete_transaction_from_last_day_by_asset(asset)
"""


def get_transaction_per_day_asset(asset):
    return get_complete_transaction_from_last_day_by_asset(asset)
