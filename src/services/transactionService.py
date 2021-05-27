from datetime import datetime

from src.data.transactionMongoUtils import get_transaction_by_id, update_transaction_by_id, \
    get_complete_transaction_from_last_day_by_asset, __MODEL_VERSION, insert_transaction
from src.helpers.dateHelper import DATE_STR
from src.services.slackEventService import send_transaction_complete_to_slack


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
        update_transaction_by_id(_id=_id, key='lastUpdate', value=datetime.now().strftime(DATE_STR))
        transaction = get_transaction_by_id(_id)
        transaction['_id'] = str(transaction['_id'])
        print('Transaction closed', transaction)
        send_transaction_complete_to_slack(str(transaction))
        return True


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


def get_complete_transaction_per_day_asset(asset):
    return get_complete_transaction_from_last_day_by_asset(asset)


def insert_transaction_event(key: str, data: dict):
    """
    [MONGODB] - [NEW TRANSACTION] ->', data)
    :param key: type of trade
    :param data: the data stored on influxDB
    :return:
    """
    dto = {
        'dateOfCreation': datetime.now().strftime(DATE_STR),
        'lastUpdate': datetime.now().strftime(DATE_STR),
        'version': __MODEL_VERSION,
        key: data
    }
    transaction_stored = insert_transaction(dto)
    return transaction_stored.inserted_id
