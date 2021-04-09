from datetime import datetime, timedelta

from src.secret.CONSTANT import __INFLUX_HOST, __INFLUX_PORT, __INFLUX_USER, __INFLUX_PASSWORD, __INFLUX_DB_TRADE_EVENT
from influxdb import InfluxDBClient

__INFLUX_CLIENT = InfluxDBClient(
    host=__INFLUX_HOST,
    port=__INFLUX_PORT,
    username=__INFLUX_USER,
    password=__INFLUX_PASSWORD,
    database=__INFLUX_DB_TRADE_EVENT
)


def getRecentEventByTypeAndAsset(asset, typeOfTrade):
    result = __INFLUX_CLIENT.query(
        'SELECT * FROM ' + __INFLUX_DB_TRADE_EVENT + '"autogen"."tradeEvent" '
        'WHERE time > now() - 2d AND asset = ' + "'" + asset + "'" +
        'AND typeOfTrade = ' + "'" + typeOfTrade + "'" +
        'GROUP BY "typeOfTrade"'
    )
    print('[INFLUXDB], querying the last recent tradeEvents ->', asset, typeOfTrade, '\n', result)
    return result


def countLastResentEvents():
    result = __INFLUX_CLIENT.query(
        'SELECT "count(*)" ' +
        'FROM "' + __INFLUX_DB_TRADE_EVENT + '"."autogen"."tradeEvent" ' +
        'WHERE time > now() - 7d GROUP BY "typeOfTrade"'
    )
    print('[INFLUXDB], counting the number of this weeks events\n', result)
    return result


def addTradeEvent(event):
    print('[INFLUXDB] writing new tradeEvent\n', event)
    __INFLUX_CLIENT.switch_database(__INFLUX_DB_TRADE_EVENT)
    __INFLUX_CLIENT.write_points(event)


def resetProductionDatabase(bool):
    if bool:
        print('\nReseting production databse, ciao datas')
        __INFLUX_CLIENT.drop_database(__INFLUX_DB_TRADE_EVENT)
        __INFLUX_CLIENT.create_database(__INFLUX_DB_TRADE_EVENT)


if __name__ == "__main__":
    tmp_db = 'tmp'
    print('Current DBs', __INFLUX_CLIENT.get_list_database())
    print('Creating :', tmp_db, ', temporary DB', '\n')
    __INFLUX_CLIENT.create_database(tmp_db)

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
    point[0]['time'] = (datetime.now() + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%SZ")
    addTradeEvent(point)
    getRecentEventByTypeAndAsset('GRT', 'buy')
    getRecentEventByTypeAndAsset('GRT', 'sell')

    __INFLUX_CLIENT.drop_database(tmp_db)
    print('\nRemoving :', tmp_db, ', temporary DB')
