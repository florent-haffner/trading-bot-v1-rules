from datetime import datetime

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from src.helpers.params import __ENVIRONMENT
from src.helpers.dateHelper import DATE_STR
from src.secret.SECRET_CONSTANT import __INFLUX_BUCKET_MARKET_EVENT, __INFLUX_URI, __INFLUX_TOKEN

__INFLUX_CLIENT = InfluxDBClient(
    url=__INFLUX_URI,
    token=__INFLUX_TOKEN,
)
__CURRENT_BUCKET = __INFLUX_BUCKET_MARKET_EVENT + '_' + __ENVIRONMENT
__INFLUXDB_CURRENT_ORG = "florent.haffner@protonmail.com"
__MEASUREMENT_NAME = "marketEvent"

__WRITE_API = __INFLUX_CLIENT.write_api(write_options=SYNCHRONOUS)
__QUERY_API = __INFLUX_CLIENT.query_api()


def build_dto(record: dict):
    """
    Build Data Transfer object with whom I'll work /w Python
    :param record: raw results of InfluxDB
    :return: a properly formatted object to interact with
    """
    return {
        'time': record['_time'],
        'measurement': record['_measurement'],
        'asset': record['asset'],
        'price': record['price'],
        'volume': record['volume']
    }


def get_all_market_events():
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
    request_results = []
    query_results = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    for table in query_results:
        if len(table.records) > 1:
            for record in table.records:
                try:
                    dto = build_dto(record)
                    request_results.append(dto)
                except KeyError:
                    return []
    print('[INFLUXDB], getAllEvents response, items length:', len(request_results))
    return request_results


def get_last_minute_market_events(asset: str, length: int):
    """
    :param asset: the asset to query
    :param length: the range of time needed
    :return: a list of the last market events
    """
    print('[INFLUXDB], getLastMinuteEvents from the last', length, 'minutes.')
    query = f"""
        from (bucket:"{__CURRENT_BUCKET}")
            |> range(start: -{length}m)
            |> filter(fn: (r) => r._measurement == "{__MEASUREMENT_NAME}")
            |> filter(fn: (r) => r.asset == "{asset}")
            |> aggregateWindow(every: 1m, fn: mean)
            |> pivot(
                    rowKey: ["_time"],
                    columnKey: ["_field"],
                    valueColumn: "_value"
            )
    """
    output_results: list = []
    request_result: list = __QUERY_API.query(org=__INFLUXDB_CURRENT_ORG, query=query)
    for table in request_result:
        if len(table.records) > 1:
            for record in table.records:
                try:
                    dto = build_dto(record)
                    dto['close'] = dto['price']
                    output_results.append(dto)
                except KeyError:
                    return []
    print('[INFLUXDB], getLastMinuteEvents response, items length:', len(output_results))
    return output_results


def insert_market_event(event: dict):
    """
    :param event: the data to write
    :return:
    """
    print('[INFLUXDB] writing new marketEvent\n', event)
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
    print('Results', get_all_market_events())
