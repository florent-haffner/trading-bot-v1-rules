import json
import re

from websocket import create_connection

from src.data.marketEventUtils import insert_market_event
from src.data.missionMongoUtils import get_all_missions


def get_asset_from_pair(asset_currency_pair: str) -> str:
    """ Handle messy 'pair' string then  return a clean string with asset """
    regex: re = re.search('([A-Z])\w+', asset_currency_pair)
    return regex.group(0)


def generate_realtime_market_dto(event: dict) -> dict:
    """
    This function handle all the mock modeling and processing before storing it on InfluxDB
    :param event:
    :return:
    """
    keys: list = ["price", "volume", "time"]
    pair: str = event[len(event) - 1]
    asset: str = get_asset_from_pair(pair)

    dto = {}
    for key in range(len(keys)):
        try:
            dto[keys[key]] = float(event[1][0][key])
        except ValueError:
            dto[keys[key]] = event[1][0][key]

    __MEASUREMENT_NAME: str = "marketEvent"
    data_object: dict = {
        'measurement': __MEASUREMENT_NAME,
        'tags': {
            'asset': asset,
            'broker': 'kraken',
        },
        'fields': dto
    }
    return data_object


def handle_market_event(ws_event: dict):
    dto = generate_realtime_market_dto(ws_event)
    insert_market_event([dto])


def bot_realtime_child_process():
    """ handle to general logic of this websocket process """
    pairs: list = []
    missions = get_all_missions()
    for mission in missions:
        for asset in mission['context']['assets']:
            pair = asset + "/" + "EUR"
            pairs.append(pair)

    websocket_data = create_connection("wss://ws.kraken.com/")
    query = {
        "event": "subscribe",
        "subscription": {"name": "trade"},
        "pair": pairs
    }
    ws_query = json.dumps(query)
    print('WS query', ws_query, type(ws_query))
    websocket_data.send(str(ws_query))

    while True:
        res = websocket_data.recv()
        event = json.loads(res)
        try:
            event_key = event.keys()
        except AttributeError:
            handle_market_event(event)


if __name__ == '__main__':
    bot_realtime_child_process()
