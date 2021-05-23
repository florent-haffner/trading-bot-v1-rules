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


def build_dto(record: dict):
    """
    :param record: raw results of InfluxDB
    :return: a properly formatted object to interact with
    """
    return {
        'time': record['_time'],
        'measurement': record['_measurement'],
        'typeOfTrade': record['typeOfTrade'],
        'asset': record['asset'],
        'price': record['price'],
        'quantity': record['quantity'],
        'transactionId': record['transactionId']
    }


def get_recent_event_by_type_and_asset(asset: str, type_of_trade: str):
    """
    [INFLUXDB], querying the last recent tradeEvents
    :param asset:
    :param type_of_trade:
    :return: a list of properly formatted objects
    """
    query = f"""
        from (bucket:"{__CURRENT_BUCKET}")
        |> range(start: -1d)
        |> filter(fn: (r) => r._measurement == "{__MEASUREMENT_NAME}")
        |> filter(fn: (r) => r.typeOfTrade == "{type_of_trade}")
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
            result = build_dto(record)
            results.append(result)
    print('[INFLUXDB], querying the last recent tradeEvents ->', asset, type_of_trade, '\n', results)
    return results


def count_all_events_from_last_seven_days():
    """
    :return: The number of events from now until 1 week ago
    """
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


def get_all_trade_events():
    """
    :return: all events from the last two days.
    """
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
                    dto = build_dto(record)
                    results.append(dto)
                except KeyError:
                    return []
    print('[INFLUXDB], getAllEvents response, items length:', len(results))
    return results


def insert_trade_event(event: dict):
    """
    Writing a new event
    :param event: dictionary to store
    :return:
    """
    print('[INFLUXDB] writing new tradeEvent\n', event)
    __WRITE_API.write(__CURRENT_BUCKET, __INFLUXDB_CURRENT_ORG, event)


def clean_trade_events():
    """
    Clean the current bucket
    :return: None
    """
    print('\nRemoving everything')
    delete_api = __INFLUX_CLIENT.delete_api()
    delete_api.delete('1970-01-01T00:00:00Z', datetime.today().strftime(DATE_STR),
                      '_measurement=' + __MEASUREMENT_NAME,
                      bucket=__CURRENT_BUCKET, org=__INFLUXDB_CURRENT_ORG)
    print('Results', get_all_trade_events())


# TODO -> not sure it's still useful
"""
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

    clean_trade_events()
"""


if __name__ == "__main__":
    # initEnvironment()

    get_recent_event_by_type_and_asset('GRT', 'buy')
    get_all_trade_events()

    # clean_trade_events()
