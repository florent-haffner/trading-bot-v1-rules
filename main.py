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
from src.helpers.params import __DEBUG, __OFFLINE, __ENVIRONMENT
from src.repository.marketEventRepository import insertMarketEvent
from src.repository.missionRepository import getAllMissions
from src.services.krakenDataService import getFormattedData, get_stocks_indicators


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
        path_csv: str = os.getcwd() + '/data/mock-' + asset + '-' + chosen_type + '.csv'
        print('Get CSV from ', path_csv)
        df = read_csv(path_csv)

    df_with_indicators: DataFrame = get_stocks_indicators(df)
    print('DF FULL - first:', datetime.fromtimestamp(df_with_indicators.head(1)['timestamp'].iloc[0]),
          'last:', datetime.fromtimestamp(df_with_indicators.tail(1)['timestamp'].iloc[-1]))

    AnalysisEngine(__DEBUG, df_with_indicators, asset, currency, length_assets, interval)

    # sleep_between_analysis: float = interval / 10
    # print('Sleeping for about', sleep_between_analysis, 'seconds.')
    # sleep(sleep_between_analysis)


def bot_realtime_child_process():

    def handle_market_event(event):
        dto = generate_dto(event)
        insertMarketEvent([dto])

    assets = []
    missions = getAllMissions()
    for mission in missions:
        for asset in mission['context']['assets']:
            pair = asset + "/" + "EUR"
            assets.append(pair)

    websocket_data = create_connection("wss://ws.kraken.com/")
    query = {
        "event": "subscribe",
        "subscription": {"name": "trade"},
        "pair": assets
    }
    mid = json.dumps(query)
    print('mid', mid, type(mid))

    websocket_data.send(str(mid))
    while True:
        res = websocket_data.recv()
        event = json.loads(res)
        try:
            event_key = event.keys()
            print(event)
        except AttributeError:
            handle_market_event(event)

def generate_dto(event):
    keys = ["price", "volume", "time", "side", "orderType"]
    dto = {
        "asset": event[len(event) - 1],
    }

    for key in range(len(keys)):
        dto[keys[key]] = event[1][0][key]

    __MEASUREMENT_NAME = "marketEvent"
    data_object = {
        'measurement': __MEASUREMENT_NAME,
        'tags': {},
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
            missions: list = list(getAllMissions())
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
