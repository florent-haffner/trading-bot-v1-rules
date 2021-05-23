import json
import os
from datetime import datetime
from multiprocessing import Process
from time import sleep
from typing import List

import pymongo.errors
from pandas import DataFrame, read_csv
from websocket import create_connection

from src.engine.analysisEngine import AnalysisEngine
from src.engine.analysisEngineHelper import get_realtime_processed_asset
from src.helpers.params import __DEBUG, __OFFLINE, __ENVIRONMENT
from src.data.marketEventUtils import insert_market_event
from src.data.missionMongoUtils import get_all_missions
from src.services.krakenDataService import getFormattedData, get_stocks_indicators
import re


def get_last_n_percentage(df, nbr_percentage) -> DataFrame:
    calculated_length: int = (len(df) * nbr_percentage) / 100
    tmp_df: DataFrame = df[int(calculated_length):]
    print('DF last -', nbr_percentage, '% - first:', datetime.fromtimestamp(tmp_df.head(1)['timestamp'].iloc[0]),
          'last:', datetime.fromtimestamp(tmp_df.tail(1)['timestamp'].iloc[-1]))
    return tmp_df


def run_bot(asset, currency, interval, length_assets):
    df: DataFrame = getFormattedData(asset + currency, str(interval))

    if __OFFLINE:
        print('DEVELOPMENT MODE')
        type_of_trade: List[str] = ['buy', 'sell']
        chosen_type: str = type_of_trade[0]
        path_csv: str = os.getcwd() + '/mock/mock-' + asset + '-' + chosen_type + '.csv'
        print('Get CSV from ', path_csv)
        df = read_csv(path_csv)

    last_market_event = get_realtime_processed_asset('ALGO')
    # last_market_event['timestamp'] = int(last_market_event['timestamp'])
    if last_market_event:
        df_last_timestamp = df.tail(1)['timestamp'].iloc[-1]
        if df_last_timestamp < last_market_event['timestamp']:
            print('Appending last_market_events processed data to dataframe')
            # Trick /w side-effect to append last_market_events at the end of the file
            df = df.append(last_market_event, ignore_index=True)

    df_with_indicators: DataFrame = get_stocks_indicators(df)
    print('DF FULL - first:', datetime.fromtimestamp(df_with_indicators.head(1)['timestamp'].iloc[0]),
          'last:', datetime.fromtimestamp(df_with_indicators.tail(1)['timestamp'].iloc[-1]))

    AnalysisEngine(__DEBUG, df_with_indicators, asset, currency, length_assets, interval)


def bot_realtime_child_process():
    def handle_market_event(ws_event: dict):
        dto = generate_dto(ws_event)
        insert_market_event([dto])

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


def generate_dto(event: dict) -> dict:
    """
    This function handle all the mock modeling and processing before storing it on InfluxDB
    :param event:
    :return:
    """
    keys: list = ["price", "volume", "time"]

    def get_asset_from_pair(asset_currency_pair: str) -> str:
        """ Handle messy 'pair' string then  return a clean string with asset """
        regex: re = re.search('([A-Z])\w+', asset_currency_pair)
        return regex.group(0)

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


def bot_main_process():
    print("[TRADING BOT ACTIVATED] - HELLO MASTER")
    if __DEBUG:
        print('SIMULATION MODE -> Exception will be raised\n')
    else:
        print('Using', __ENVIRONMENT, 'environment -> Exception will stay silent\n')
    sleep(1)

    while True:
        try:
            startMissionQuery = datetime.now()
            missions: list = list(get_all_missions())
            endMissionQuery = datetime.now()

            time_diff: int = int((endMissionQuery - startMissionQuery).total_seconds() * 1000)
            print('Executed MongoDB in', time_diff, 'ms')

            for mission in missions:
                assets: str = mission['context']['assets']
                interval: int = mission['context']['interval']
                print('[ASSETS TO QUERY] :', assets)
                for asset in assets:
                    currency: str = 'EUR'
                    startBotAnalysis = datetime.now()
                    run_bot(asset, currency, interval, len(assets))
                    endBotAnalysis = datetime.now()
                    time_diff: int = int((endBotAnalysis - startBotAnalysis).total_seconds() * 1000)
                    print('Executed bot analysis in', time_diff, 'ms')

                time_to_sleep: float = interval * 10
                endPipeline = datetime.now()
                time_diff: int = int((endPipeline - startMissionQuery).total_seconds() * 1000)
                print('Executed full pipeline in', time_diff, 'ms')

                print('Sleeping for about', time_to_sleep, 'seconds.')
                sleep(time_to_sleep)

        except pymongo.errors.ServerSelectionTimeoutError:
            sleep(10)


def start_multiprocess_bot():
    t1 = Process(target=bot_main_process)
    t2 = Process(target=bot_realtime_child_process)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    start_multiprocess_bot()
