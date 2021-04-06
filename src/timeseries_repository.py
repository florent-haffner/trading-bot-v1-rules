from datetime import datetime

from CONSTANT import __INFLUX_HOST, __INFLUX_PORT, __INFLUX_USER, __INFLUX_PASSWORD, __INFLUX_DB_TRADE_EVENT
from influxdb import InfluxDBClient

__INFLUX_CLIENT = InfluxDBClient(
    host=__INFLUX_HOST,
    port=__INFLUX_PORT,
    username=__INFLUX_USER,
    password=__INFLUX_PASSWORD
)


def addStockActions(event):
    print('\nsaving real db events', event)
    __INFLUX_CLIENT.switch_database(__INFLUX_DB_TRADE_EVENT)
    __INFLUX_CLIENT.write_points(event)

    query = __INFLUX_CLIENT.query('SELECT "quantity" '
                                  'FROM "ts_trade_event"."autogen"."tradeEvents" '
                                  'WHERE time > now() - 4d GROUP BY "typeOfTrade"')
    print('query real ts', query)


def getLastTradeEventByType(typeOfTrade):
    pass


def test_trade_event_DB(database):
    print('Querying the real ts database')
    __INFLUX_CLIENT.create_database(database)

    points = [
        {
            'measurement': 'tradeEvent',
            'time': "2021-04-05T8:01:00Z",
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
            'time': "2021-04-05T8:01:00Z",
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
    # __INFLUX_CLIENT.switch_database(tmp_DB)
    # __INFLUX_CLIENT.write_points(json_body)
    #
    # query = __INFLUX_CLIENT.query('SELECT "duration" '
    #                               'FROM "timeseries"."autogen"."brushEvents" '
    #                               'WHERE time > now() - 4d GROUP BY "user"')
    # print('querying brushEvent ->', query)

    print('\nsaving real db events', points)
    __INFLUX_CLIENT.switch_database(__INFLUX_DB_TRADE_EVENT)
    __INFLUX_CLIENT.write_points(points)

    query = __INFLUX_CLIENT.query('SELECT "quantity" '
                                  'FROM "ts_trade_event"."autogen"."tradeEvent" '
                                  'WHERE time > now() - 4d GROUP BY "typeOfTrade"')
    print('query real ts', query)

    # addStockActions(points)
    # getLastTradeEventByType('buy')


def getAllStockActions():
    query = 'SELECT "volume" FROM ' + __INFLUX_DB_TRADE_EVENT + '."autogen"."brushEvents" WHERE time > now() - 5d GROUP BY "user"'
    res = __INFLUX_CLIENT.query(query)
    print(res)





def initial_config():
    print('[InfluxDB] Initial config')

    __INFLUX_CLIENT.create_database(__INFLUX_DB_TRADE_EVENT)
    print('DBs', __INFLUX_CLIENT.get_list_database())


def tmp_last_points_query(tmp_DB):
    __INFLUX_CLIENT.drop_database(tmp_DB)
    __INFLUX_CLIENT.create_database(tmp_DB)
    print(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"), 'vs', "2021-04-05T8:01:00Z\n")
    json_body = [
        {
            "measurement": "brushEvents",
            "tags": {
                "user": "Carol",
                "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
            },
            "time": "2021-04-05T8:01:00Z",
            "fields": {
                "duration": 127
            }
        },
        {
            "measurement": "brushEvents",
            "tags": {
                "user": "Carol",
                "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
            },
            "time": "2021-04-05T8:01:00Z",
            "fields": {
                "duration": 132
            }
        },
        {
            "measurement": "brushEvents",
            "tags": {
                "user": "Carol",
                "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
            },
            "time": "2021-04-05T8:01:00Z",
            "fields": {
                "duration": 129
            }
        }
    ]
    __INFLUX_CLIENT.switch_database(tmp_DB)
    __INFLUX_CLIENT.write_points(json_body)

    query = __INFLUX_CLIENT.query('SELECT "duration" '
                                  'FROM "timeseries"."autogen"."brushEvents" '
                                  'WHERE time > now() - 4d GROUP BY "user"')
    print('querying brushEvent ->', query)






if __name__ == "__main__":
    initial_config()

    tmp_DB = 'timeseries'
    tmp_last_points_query(tmp_DB)

    test_trade_event_DB(__INFLUX_DB_TRADE_EVENT)
