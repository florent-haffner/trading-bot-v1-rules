from datetime import datetime, timedelta

# from influxdb import InfluxDBClient  # TODO -> remove after changing DB to v2
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from src.helpers.CONSTANT import DATE_STR
from src.secret.SECRET_CONSTANT import __INFLUX_HOST, __INFLUX_PORT, __INFLUX_USER, __INFLUX_PASSWORD, \
    __INFLUX_DB_TRADE_EVENT, __INFLUX_URI, __INFLUX_TOKEN

# __INFLUX_CLIENT = None
# __CURRENT_BUCKET = None

__CURRENT_BUCKET = __INFLUX_DB_TRADE_EVENT + '_dev'
__INFLUX_CLIENT = InfluxDBClient(
    url=__INFLUX_URI,
    token=__INFLUX_TOKEN,
)
__INFLUXDB_CURRENT_ORG = "florent.haffner@protonmail.com"
__WRITE_API = __INFLUX_CLIENT.write_api(write_options=SYNCHRONOUS)
__QUERY_API = __INFLUX_CLIENT.query_api()
__MEASUREMENT_NAME = "tradeEvent"

# if __INFLUX_URI:
# else:
#     __CURRENT_BUCKET = __INFLUX_DB_TRADE_EVENT + '_dev'
#     __INFLUX_CLIENT = InfluxDBClient(
#         host=__INFLUX_HOST,
#         port=__INFLUX_PORT,
#         username=__INFLUX_USER,
#         password=__INFLUX_PASSWORD,
#         database=__CURRENT_BUCKET
#     )



def getRecentEventByTypeAndAsset(asset, typeOfTrade):
    result = __INFLUX_CLIENT.query(
        'SELECT * FROM ' + __CURRENT_BUCKET + '"autogen"."tradeEvent" '
        'WHERE time > now() - 2d AND asset = ' + "'" + asset + "'" +
        'AND typeOfTrade = ' + "'" + typeOfTrade + "'" +
        'GROUP BY "typeOfTrade"'
    )
    print('[INFLUXDB], querying the last recent tradeEvents ->', asset, typeOfTrade, '\n', result)
    return result


def countAllEvents():
    result = __INFLUX_CLIENT.query(
        'SELECT "count(*)" ' +
        'FROM "' + __CURRENT_BUCKET + '"."autogen"."tradeEvent" ' +
        'WHERE time > now() - 7d GROUP BY "typeOfTrade"'
    )
    print('[INFLUXDB], counting the number of this weeks events\n', result)
    return result


def getAllEvents():
    result = __INFLUX_CLIENT.query(
        'SELECT * ' +
        'FROM "' + __CURRENT_BUCKET + '"."autogen"."tradeEvent" ' +
        'WHERE time > now() - 7d GROUP BY "typeOfTrade"'
    )
    print('[INFLUXDB], counting the number of this weeks events\n', result)
    return result


def insertTradeEvent(event):
    print('[INFLUXDB] writing new tradeEvent\n', event)
    __INFLUX_CLIENT.switch_database(__CURRENT_BUCKET)
    __INFLUX_CLIENT.write_points(event)


def cleanTradeEvents():
    print('\nReseting production databse, ciao datas')
    __INFLUX_CLIENT.drop_database(__CURRENT_BUCKET)
    __INFLUX_CLIENT.create_database(__CURRENT_BUCKET)


def initEnvironment():
    tmp_db = 'tmp'
    # print('InfluxDB HEALTH', __INFLUX_CLIENT.health())

    print('Current DBs', __INFLUX_CLIENT.get_list_database())
    print('Creating :', tmp_db, ', temporary DB', '\n')
    __INFLUX_CLIENT.create_database(tmp_db)

    point = [
        {
            'measurement': 'tradeEvent',
            'tags': {'typeOfTrade': 'buy'},
            'fields': {
                'asset': 'GRT',
                'quantity': 32.,
                'price': 32.
            },
            'time': (datetime.now() + timedelta(hours=2)).strftime(DATE_STR),
        }
    ]

    insertTradeEvent(point)
    point[0]['time'] = (datetime.now() + timedelta(hours=4)).strftime(DATE_STR)
    insertTradeEvent(point)
    getRecentEventByTypeAndAsset('GRT', 'buy')
    getRecentEventByTypeAndAsset('GRT', 'sell')

    __INFLUX_CLIENT.drop_database(tmp_db)
    print('\nRemoving :', tmp_db, ', temporary DB')

    getRecentEventByTypeAndAsset('GRT', 'buy')


if __name__ == "__main__":
    # initEnvironment()

    # INIT ENV
    point = [
        {
            'measurement': __MEASUREMENT_NAME,
            'tags': {'typeOfTrade': 'buy'},
            'fields': {
                'asset': 'GRT',
                'quantity': 32.,
                'price': 32.
            }
        }
    ]
    __WRITE_API.write(__CURRENT_BUCKET, __INFLUXDB_CURRENT_ORG, point)

    # Update the point the write a new one
    # point[0]['time'] = (datetime.now() + timedelta(hours=2)).strftime(DATE_STR)
    __WRITE_API.write(__CURRENT_BUCKET, __INFLUXDB_CURRENT_ORG, point)


    # GET EVERYTHING
    query = ' from (bucket:"ts_trade_event_dev")\
        |> range(start: -2d)\
        |> filter(fn: (r) => r._measurement == "tradeEvent")\
        |> filter(fn: (r) => r.typeOfTrade == "buy" )'
    result_db_request = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    print(result_db_request)
    results = []
    for table in result_db_request:
        for record in table.records:
            print(record)
            results.append( (record.get_field(), record.get_value()) )
    print(results)

    # REMOVE EVERYTHING
    query = ' from (bucket:"ts_trade_event_dev")\
        |> range(start: -2d)\
        |> drop(fn: (column) => column =~ /.*/ )'

    # GET EVERYTHING
    result_db_request = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    print(result_db_request)
    results = []
    for table in result_db_request:
        for record in table.records:
            print(record)
            results.append( (record.get_field(), record.get_value()) )
    print(results)

    # cleanTradeEvents()

    pass
