from datetime import datetime

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from src.helpers.params import __ENVIRONMENT
from src.helpers.dateHelper import DATE_STR
from src.secret.SECRET_CONSTANT import __INFLUX_BUCKET_TRADE_EVENT, __INFLUX_URI, __INFLUX_TOKEN

__INFLUX_CLIENT = InfluxDBClient(
    url=__INFLUX_URI,
    token=__INFLUX_TOKEN,
)
__CURRENT_BUCKET = __INFLUX_BUCKET_TRADE_EVENT + '_' + __ENVIRONMENT
__INFLUXDB_CURRENT_ORG = "florent.haffner@protonmail.com"
__MEASUREMENT_NAME = "tradeEvent"

__WRITE_API = __INFLUX_CLIENT.write_api(write_options=SYNCHRONOUS)
__QUERY_API = __INFLUX_CLIENT.query_api()



def buildDTO(record):
    result = {
        'time': record['_time'],
        'measurement': record['_measurement'],
        'typeOfTrade': record['typeOfTrade'],
        'asset': record['asset'],
        'price': record['price'],
        'quantity': record['quantity'],
        'transactionId': record['transactionId']
    }
    return result


def getRecentEventByTypeAndAsset(asset, typeOfTrade):
    query = f"""
        from (bucket:"{__CURRENT_BUCKET}")
        |> range(start: -1d)
        |> filter(fn: (r) => r._measurement == "{__MEASUREMENT_NAME}")
        |> filter(fn: (r) => r.typeOfTrade == "{typeOfTrade}")
        |> pivot(
            rowKey: ["_time"],
            columnKey: ["_field"],
            valueColumn: "_value"
        )
        |> filter(fn: (r) => r.asset == "{asset}")
    """
    request_result = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    results = []
    for table in request_result:
        for record in table.records:
            result = buildDTO(record)
            results.append(result)
    print('[INFLUXDB], querying the last recent tradeEvents ->', asset, typeOfTrade, '\n', results)
    return results


def countAllEvents():
    print('[INFLUXDB], count event from the last seven days.')
    query = f"""
        from (bucket:"{__CURRENT_BUCKET}")
            |> range(start: -7d)
            |> pivot(
                rowKey: ["_time"],
                columnKey: ["_field"],
                valueColumn: "_value"
            )
    """

    countEvents = 0
    request_result = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    for table in request_result:
        countEvents = len(table.records)
    print('[INFLUXDB], events in the last 7 days:', countEvents)
    return countEvents


def getAllEvents():
    print('[INFLUXDB], getAllEvents from the last two days.')
    query = f"""
        from (bucket:"{__CURRENT_BUCKET}")
            |> range(start: -2d)
            |> filter(fn: (r) => r._measurement == "{__MEASUREMENT_NAME}")
            |> pivot(
                    rowKey: ["_time"],
                    columnKey: ["_field"],
                    valueColumn: "_value"
            )
    """
    results = []
    request_result = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    for table in request_result:
        if len(table.records) > 1:
            for record in table.records:
                try:
                    dto = buildDTO(record)
                    results.append(dto)
                except KeyError:
                    return []
    print('[INFLUXDB], getAllEvents response, items length:', len(results))
    return results


def insertTradeEvent(event):
    print('[INFLUXDB] writing new tradeEvent\n', event)
    __WRITE_API.write(__CURRENT_BUCKET, __INFLUXDB_CURRENT_ORG, event)


def cleanTradeEvents():
    print('\nRemoving everything')
    delete_api = __INFLUX_CLIENT.delete_api()
    delete_api.delete('1970-01-01T00:00:00Z', datetime.today().strftime(DATE_STR),
                      '_measurement=' + __MEASUREMENT_NAME,
                      bucket=__CURRENT_BUCKET, org=__INFLUXDB_CURRENT_ORG)
    print('Results', getAllEvents())


def initEnvironment():
    from time import sleep
    print('INIT ENV - test and documentation purpose\n')
    getAllEvents()

    point = [
        {
            'measurement': __MEASUREMENT_NAME,
            'tags': {'typeOfTrade': 'buy'},
            'fields': {
                'asset': 'GRT',
                'quantity': 32.,
                'price': 32.,
                'transactionId': 'lol'
            }
        }

    ]
    insertTradeEvent(point)
    sleep(1)

    point[0]['fields']['asset'] = "ALGO"
    insertTradeEvent(point)
    sleep(1)

    point[0]['fields']['asset'] = "ALGO"
    insertTradeEvent(point)
    sleep(1)

    point[0]['fields']['asset'] = "LINK"
    insertTradeEvent(point)
    sleep(1)

    getRecentEventByTypeAndAsset('ETH', 'buy')

    getAllEvents()

    # Trying to understand the date format used by InfluxDB
    res = getRecentEventByTypeAndAsset('GRT', 'buy')
    last_date = res[0]['time']
    print('last_date')
    print(last_date, 'STRING', str(last_date), type(last_date))
    sleep(1)

    countAllEvents()
    getRecentEventByTypeAndAsset(asset='GRT', typeOfTrade='buy')

    cleanTradeEvents()


if __name__ == "__main__":
    # initEnvironment()

    getRecentEventByTypeAndAsset('GRT', 'buy')
    getAllEvents()

    # cleanTradeEvents()
