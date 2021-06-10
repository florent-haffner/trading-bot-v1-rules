from datetime import datetime, timedelta

from src.data.marketEventUtils import get_ohlc_data_from_market_events
from src.data.tradeEventUtils import get_recent_event_by_type_and_asset, insert_trade_event
from src.helpers.dateHelper import DATE_UTC_TZ_STR, set_timezone
from src.services.krakenPrivateTradeService import create_new_order
from src.services.slackEventService import send_trade_event_to_slack, create_trade_event_message, \
    send_exception_to_slack
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
    if order_response['error']:
        formatted_error: str = str(order_response) + '->' + str(order_response)
        send_exception_to_slack(formatted_error)

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
        result = update_to_complete_transaction(_id=transaction_id, key=type_of_trade, points=point)
        if result:
            success = handle_trade_data_and_logic(point=point, asset=asset, currency=currency,
                                                  type_of_trade=type_of_trade, quantity=quantity)
    return success


class Node:
    """ Object that represent the current last node and it's friend before it. """
    def __init__(self, item_data: dict, previous_node: object):
        """ ATTRIBUTES """
        self.previous_node = previous_node
        # Time is on current timezone then calculated to follow Kraken's standard
        self.time = set_timezone(item_data['time']) - timedelta(minutes=5)
        self.open = item_data['open']
        self.high = item_data['high']
        self.low = item_data['low']
        self.close = item_data['close']
        self.index = 0
        # Current trend evolution attributes
        self.nbr_previous_positive = 0
        self.nbr_previous_negative = 0
        self.trade_event = 'waiting'

        """ METHOD """
        # TODO -> only use during DEBUG
        # self.print_current_trend()

        try:
            self.calculate_trend_evolution()
        except AttributeError:
            # Probably the first ndoe
            pass

    def __repr__(self):
        return '{ time: ' + str(self.time) + \
               ', open: ' + str(self.open) + \
               ', close: ' + str(self.close) + \
               ', high: ' + str(self.high) + \
               ', low: ' + str(self.low) + ' ' + \
               ', nbr_positive: ' + str(self.nbr_previous_positive) + ' ' + \
               ', nbr_negative: ' + str(self.nbr_previous_negative) + ' ' + \
               ', trade_Event: ' + self.trade_event + ' ' + \
               '}'

    def print_current_trend(self):
        print('\nNEW NODE', self.time)
        print('open', self.open)
        print('low', self.low, 'delta', self.low * 100 / self.open)
        print('high', self.high, 'delta', self.high * 100 / self.open)
        print('close', self.close, 'delta', self.close * 100 / self.open)

    def calculate_trend_evolution(self):
        # Trend management
        if self.close > self.previous_node.close:
            self.nbr_previous_positive = self.previous_node.nbr_previous_positive + 1
        if self.close < self.previous_node.close:
            self.nbr_previous_negative = self.previous_node.nbr_previous_negative + 1

        # Trade management
        if self.close < self.high:
            self.trade_event = 'sell'

        if self.nbr_previous_negative > 2:
            self.trade_event = 'buy'

def generate_graph_from_ohlc(data: list) -> list:
    graph: list = []
    previous_node: object = None
    for time_window in data:
        current_node = Node(time_window, previous_node)
        graph.append(current_node)
        previous_node = current_node

    node_analysis(current_node)

    return graph


def node_analysis(node: Node):
    if node.trade_event is not 'waiting':
        print(node)
    node_analysis(node.previous_node)


if __name__ == '__main__':
    nbr_hour: int = 6
    length_in_minute: int = 5 * 12 * nbr_hour
    results = get_ohlc_data_from_market_events(
        asset='LINK',
        measurement='price',
        interval=5,
        length_in_minute=length_in_minute
    )
    from pandas import DataFrame
    import matplotlib.pyplot as plt
    df = DataFrame(results)
    df.plot('time', 'close')
    plt.show()

    graph = generate_graph_from_ohlc(results)
