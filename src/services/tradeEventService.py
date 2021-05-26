from datetime import datetime

from src.data.tradeEventUtils import get_recent_event_by_type_and_asset, insert_trade_event
from src.helpers.dateHelper import DATE_UTC_TZ_STR
from src.services.krakenPrivateTradeService import create_new_order
from src.services.slackEventService import send_trade_event_to_slack, create_trade_event_message
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


def handle_trade_data_and_logic(point: dict, asset: str, currency: str, type_of_trade: str, quantity: float):
    """
    Wrap interaction with Kraken API, Slack API and InfluxDB
    :param point: InfluxDB dictionary
    :param asset: crypto-asset
    :param currency: EUR
    :param type_of_trade: buy/sell
    :param quantity: the number of asset to buy
    :return: success of the operation
    """
    # TODO -> must add error handling to structured even more this part of the code
    del point['time']
    order_params = asset + currency, type_of_trade, quantity
    order_response = create_new_order(pair=order_params[0], type=order_params[1], quantity=order_params[2])
    print('Kraken response', order_response)

    msg = create_trade_event_message(title='New trade event - ' + order_params[1],
                                     input_params=str(order_params),
                                     results=order_response)
    send_trade_event_to_slack(msg)

    insert_trade_event([point])
    return True


def add_trade_event(type_of_trade: str, quantity: float, asset: str,
                    interval: int, transaction_id: str, price: float, currency: str):
    """
    Link everything together and add a transaction before storing the tradeEvent on InfluxDB
    :param type_of_trade: 
    :param quantity: 
    :param asset: 
    :param interval: 
    :param transaction_id: 
    :param price:
    :param currency:
    :return: a bool to know if the transaction is a success
    """
    success = False
    point = generate_trade_event_dto(type_of_trade=type_of_trade, quantity=quantity,
                                     asset=asset, interval=interval, price=price)

    if not transaction_id:
        transaction_id = insert_transaction_event(type_of_trade, point)
    point['fields']['transactionId'] = str(transaction_id)

    if type_of_trade == 'buy':
        success = handle_trade_data_and_logic(point=point, asset=asset, currency=currency,
                                              type_of_trade=type_of_trade, quantity=quantity)

    # Upgrading previous transaction on MongoDB
    if type_of_trade == 'sell':
        print('Updating', transaction_id, 'to complete transaction')
        result = update_to_complete_transaction(_id=transaction_id, key=type_of_trade, points=point)
        if result:
            success = handle_trade_data_and_logic(point=point, asset=asset, currency=currency,
                                                  type_of_trade=type_of_trade, quantity=quantity)
    return success
