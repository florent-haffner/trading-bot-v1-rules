from datetime import datetime

from src.data.tradeEventUtils import get_recent_event_by_type_and_asset, insert_trade_event
from src.helpers.dateHelper import DATE_UTC_TZ_STR
from src.services.transactionService import update_to_complete_transaction, insert_transaction_event


def get_last_trade_event_by_type_and_asset(asset, type_of_trade):
    """
    :param asset: the asset to query
    :param type_of_trade: the type_of_trade to specify the query
    :return: the most recent trade event on InfluxDB
    """
    print('Get last event by type', type_of_trade, 'and asset:', asset)
    result = get_recent_event_by_type_and_asset(asset, type_of_trade)
    most_recent = None
    for item in result:
        if not most_recent:
            most_recent = item
        if most_recent:
            if item['time'] > most_recent['time']:
                most_recent = item
    return most_recent


def generate_trade_event_dto(type_of_trade, quantity, asset, interval, price):
    """
    :param type_of_trade: 
    :param quantity: 
    :param asset: 
    :param interval: 
    :param price: 
    :return: A Data Transfer Object with the structure InfluxDB need
    """
    return {
        'time': datetime.strftime(datetime.now(), DATE_UTC_TZ_STR),
        'measurement': 'tradeEvent',
        'tags': {
            'typeOfTrade': type_of_trade,
            'interval': interval
        },
        'fields': {
            'asset': asset,
            'quantity': quantity,
            'price': price
        }
    }


def add_trade_event(type_of_trade, quantity, asset, interval, transaction_id, price):
    """
    Link everything together and add a transaction before storing the tradeEvent on InfluxDB
    :param type_of_trade: 
    :param quantity: 
    :param asset: 
    :param interval: 
    :param transaction_id: 
    :param price: 
    :return: a bool to know if the transaction is a success
    """
    success = False
    point = generate_trade_event_dto(type_of_trade=type_of_trade, quantity=quantity,
                                     asset=asset, interval=interval, price=price)

    if not transaction_id:
        transaction_id = insert_transaction_event(type_of_trade, point)
    point['fields']['transactionId'] = str(transaction_id)

    if type_of_trade == 'buy':
        # Adding new tradeEvent on InfluxDB
        del point['time']
        insert_trade_event([point])
        success = True

    # Upgrading previous transaction on MongoDB
    if type_of_trade == 'sell':
        print('Updating', transaction_id, 'to complete transaction')
        result = update_to_complete_transaction(_id=transaction_id,
                                                key=type_of_trade,
                                                points=point)
        if result:
            del point['time']
            insert_trade_event([point])
            success = True
    return success
