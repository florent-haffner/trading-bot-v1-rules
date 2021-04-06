from datetime import datetime, timedelta

from CONSTANT import __INFLUX_HOST, __INFLUX_PORT, __INFLUX_USER, __INFLUX_PASSWORD, __INFLUX_DB_TRADE_EVENT
from influxdb import InfluxDBClient

__INFLUX_CLIENT = InfluxDBClient(
    host=__INFLUX_HOST,
    port=__INFLUX_PORT,
    username=__INFLUX_USER,
    password=__INFLUX_PASSWORD
)


def getRecentEventByTypeAndAsset(asset):
    query = __INFLUX_CLIENT.query(
        'SELECT * FROM ' + __INFLUX_DB_TRADE_EVENT + '"autogen"."tradeEvent" '
        'WHERE time > now() - 2d AND asset = ' + "'" + asset + "'" +
        'GROUP BY "typeOfTrade"'
    )
    print('[INFLUXDB], querying the last recent tradeEvents\n', query)


def countLastResentEvents():
    query = __INFLUX_CLIENT.query('SELECT "count(*)" '
                                  'FROM "' + __INFLUX_DB_TRADE_EVENT + '"."autogen"."tradeEvent" '
                                   'WHERE time > now() - 7d GROUP BY "typeOfTrade"')
    print('[INFLUXDB], counting the number of this weeks events\n', query)


def addTradeEvent(event):
    print('[INFLUXDB] writing new tradeEvent\n', event)
    __INFLUX_CLIENT.switch_database(__INFLUX_DB_TRADE_EVENT)
    __INFLUX_CLIENT.write_points(event)


if __name__ == "__main__":
    print('Current DBs', __INFLUX_CLIENT.get_list_database(), '\n')
    __INFLUX_CLIENT.drop_database(__INFLUX_DB_TRADE_EVENT)
    __INFLUX_CLIENT.create_database(__INFLUX_DB_TRADE_EVENT)

    point = [
        {
            'measurement': 'tradeEvent',
            'time': (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'tags': {
                'typeOfTrade': 'buy'
            },
            'fields': {
                'asset': 'GRT',
                'quantity': 32.,
                'price': 32.,
                'acknowledge': False
            }
        }
    ]

    addTradeEvent(point)
    getRecentEventByTypeAndAsset('GRT')
