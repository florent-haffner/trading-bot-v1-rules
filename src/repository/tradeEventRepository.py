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
    delete_api = __INFLUX_CLIENT.delete_api()
    # GET EVERYTHING
    query = """
        from (bucket:"ts_trade_event_dev")\
        |> range(start: -2d)\
        |> filter(fn: (r) => r._measurement == "tradeEvent")\
        |> filter(fn: (r) => r.typeOfTrade == "buy" )
    """

    result_db_request = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    results = []
    for table in result_db_request:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    print('initial env', results)

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

    result_db_request = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    results = []
    for table in result_db_request:
        for record in table.records:
            results.append( (record.get_field(), record.get_value()) )
    print('result', results)

    delete_api.delete('1970-01-01T00:00:00Z', datetime.today().strftime(DATE_STR),
                      '_measurement=' + __MEASUREMENT_NAME,
                      bucket=__CURRENT_BUCKET, org=__INFLUXDB_CURRENT_ORG)


    result_db_request = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    results = []
    for table in result_db_request:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    print('Remove everything', results)


if __name__ == "__main__":
    initEnvironment()

    # cleanTradeEvents()

    pass
