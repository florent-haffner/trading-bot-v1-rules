from datetime import datetime

from src.data.tradeEventUtils import get_recent_event_by_type_and_asset, insert_trade_event
from src.data.transactionMongoUtils import insert_transaction_event
from src.helpers.dateHelper import DATE_UTC_TZ_STR
from src.services.krakenTradeService import get_last_price
from src.services.transactionService import update_to_complete_transaction


def get_last_trade_event_by_type_and_asset(asset, type_of_trade):
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


def generate_trade_event_dto(type_of_trade, volume_to_buy, asset, interval, price):
    return {
        'time': datetime.strftime(datetime.now(), DATE_UTC_TZ_STR),
        'measurement': 'tradeEvent',
        'tags': {
            'typeOfTrade': type_of_trade,
            'interval': interval
        },
        'fields': {
            'asset': asset,
            'quantity': volume_to_buy,
            'price': price
        }
    }


def add_trade_event(type_of_trade, volume_to_buy, asset, interval, currency, transaction_id):
    success = False
    price = get_last_price(asset, currency)
    point = generate_trade_event_dto(type_of_trade=type_of_trade, volume_to_buy=volume_to_buy,
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
