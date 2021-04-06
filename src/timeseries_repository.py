from datetime import datetime, timedelta

from CONSTANT import __INFLUX_HOST, __INFLUX_PORT, __INFLUX_USER, __INFLUX_PASSWORD, __INFLUX_DB_TRADE_EVENT
from influxdb import InfluxDBClient

__INFLUX_CLIENT = InfluxDBClient(
    host=__INFLUX_HOST,
    port=__INFLUX_PORT,
    username=__INFLUX_USER,
    password=__INFLUX_PASSWORD
)


def getRecentEventByType():
    # query = __INFLUX_CLIENT.query('SELECT "quantity, price, acknowledge" '
    #                               'FROM "' + __INFLUX_DB_TRADE_EVENT + '"."autogen"."tradeEvent" '
    #                               'WHERE time > now() - 2d GROUP BY "typeOfTrade"')
    # print('[INFLUXDB], querying last event\n', query)

    test_query = __INFLUX_CLIENT.query(
        'SELECT * FROM ' + __INFLUX_DB_TRADE_EVENT + '"autogen"."tradeEvent" WHERE time > now() - 2d GROUP BY "typeOfTrade"')
    print('test', test_query)


def countLastResentEvents():
    query = __INFLUX_CLIENT.query('SELECT "count(*)" '
                                  'FROM "' + __INFLUX_DB_TRADE_EVENT + '"."autogen"."tradeEvent" '
                                   'WHERE time > now() - 7d GROUP BY "typeOfTrade"')
    print('Return the number of last weeks events', query)


def addTradeEvent(event):
    print('[INFLUXDB] writing new tradeEvent', event)
    __INFLUX_CLIENT.switch_database(__INFLUX_DB_TRADE_EVENT)
    __INFLUX_CLIENT.write_points(event)

    query = __INFLUX_CLIENT.query('SELECT "quantity, price, acknowledge" '
                                  'FROM "' + __INFLUX_DB_TRADE_EVENT + '"."autogen"."tradeEvent" '
                                                                       'WHERE time > now() - 2d GROUP BY "typeOfTrade"')
    print('query inside add function', query)


def initial_config():
    print('[InfluxDB] Initial config')

    __INFLUX_CLIENT.create_database(__INFLUX_DB_TRADE_EVENT)
    print('DBs', __INFLUX_CLIENT.get_list_database())



def test_trade_event_DB(database):
    print('Querying the real ts database')
    # __INFLUX_CLIENT.drop_database(database)
    # __INFLUX_CLIENT.create_database(database)

    points = [
        {
            'measurement': 'tradeEvent',
            'time': (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'tags': {
                'typeOfTrade': 'buy',
            },
            'fields': {
                'quantity': 32,
                'price': 32,
                'acknowledge': False
            }
        },
        {
            'measurement': 'tradeEvent',
            'time': (datetime.now() + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'tags': {
                'typeOfTrade': 'buy',
            },
            'fields': {
                'quantity': 32,
                'price': 32,
                'acknowledge': False
            }
        }
    ]

    print('\nsaving real db events', points)
    __INFLUX_CLIENT.switch_database(__INFLUX_DB_TRADE_EVENT)
    __INFLUX_CLIENT.write_points(points)

    test_query = __INFLUX_CLIENT.query('SELECT * FROM ' + __INFLUX_DB_TRADE_EVENT + '"autogen"."tradeEvent" WHERE time > now() - 2d GROUP BY "typeOfTrade"')
    print('test', test_query)

    query = __INFLUX_CLIENT.query('SELECT "quantity, price, acknowledge" '
                                  'FROM "' + __INFLUX_DB_TRADE_EVENT + '"."autogen"."tradeEvent" '
                                  'WHERE time > now() - 5d GROUP BY "typeOfTrade"')
    print('query real ts', query)


def countLastResentEvents():
    query = __INFLUX_CLIENT.query('SELECT "count(*)" '
                                  'FROM "' + __INFLUX_DB_TRADE_EVENT + '"."autogen"."tradeEvent" '
                                   'WHERE time > now() - 7d GROUP BY "typeOfTrade"')
    print('Return the number of last weeks events', query)


def addTradeEvent(event):
    print('[INFLUXDB] writing new tradeEvent', event)
    __INFLUX_CLIENT.switch_database(__INFLUX_DB_TRADE_EVENT)
    __INFLUX_CLIENT.write_points(event)

    query = __INFLUX_CLIENT.query('SELECT "quantity, price, acknowledge" '
                                  'FROM "' + __INFLUX_DB_TRADE_EVENT + '"."autogen"."tradeEvent" '
                                  'WHERE time > now() - 2d GROUP BY "typeOfTrade"')
    print('query inside add function', query)


def initial_config():
    print('[InfluxDB] Initial config')

    __INFLUX_CLIENT.create_database(__INFLUX_DB_TRADE_EVENT)
    print('DBs', __INFLUX_CLIENT.get_list_database())


if __name__ == "__main__":
    initial_config()

    __INFLUX_CLIENT.drop_database(__INFLUX_DB_TRADE_EVENT)
    __INFLUX_CLIENT.create_database(__INFLUX_DB_TRADE_EVENT)
    DTO = [
        {
            'measurement': 'tradeEvent',
            'time': (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'tags': {
                'typeOfTrade': 'buy',
            },
            'fields': {
                'quantity': 32.,
                'price': 32.,
                'acknowledge': False
            }
        }
    ]
    addTradeEvent(DTO)
    getRecentEventByType()

    # test_trade_event_DB(__INFLUX_DB_TRADE_EVENT)
