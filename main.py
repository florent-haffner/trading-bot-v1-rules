import os
from datetime import datetime
from multiprocessing import Process
from time import sleep

import pymongo.errors
from pandas import DataFrame, read_csv

from src.engine.analysisEngine import AnalysisEngine
from src.engine.analysisEngineHelper import query_realtime_processed_by_asset
from src.helpers.emailSenderHelper import send_email
from src.helpers.params import __DEBUG, __OFFLINE, __ENVIRONMENT
from src.data.missionMongoUtils import get_all_missions
from src.services.krakenPublicDataService import get_formatted_data, get_stocks_indicators

from src.services.krakenRealtimeMarketService import bot_realtime_child_process


class UnableToConnectMongoDBInstanceException(Exception):
    """ Failed to connect to Mongo so raise an error """
    super(Exception)


def get_last_n_percentage(df, nbr_percentage) -> DataFrame:
    calculated_length: int = (len(df) * nbr_percentage) / 100
    tmp_df: DataFrame = df[int(calculated_length):]
    print('DF last -', nbr_percentage, '% - first:', datetime.fromtimestamp(tmp_df.head(1)['timestamp'].iloc[0]),
          'last:', datetime.fromtimestamp(tmp_df.tail(1)['timestamp'].iloc[-1]))
    return tmp_df


def run_bot(asset: str, currency: str, interval: int, length_assets: int):
    df: DataFrame = get_formatted_data(asset + currency, str(interval))

    if __OFFLINE:
        print('DEVELOPMENT MODE')
        type_of_trade: list = ['buy', 'sell']
        chosen_type: str = type_of_trade[0]
        path_csv: str = os.getcwd() + '/src/mock/mock-' + asset + '-' + chosen_type + '.csv'
        print('Get CSV from ', path_csv)
        df = read_csv(path_csv)

    last_market_event = query_realtime_processed_by_asset('ALGO')
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


def bot_main_process():
    print("[TRADING BOT ACTIVATED] - HELLO MASTER")
    if __DEBUG:
        print('SIMULATION MODE -> Exception will be raised\n')
    else:
        print('Using', __ENVIRONMENT, 'environment -> Exception will stay silent\n')
    sleep(1)

    while True:
        nbr_mongo_try: int = 0
        try:
            startMissionQuery = datetime.now()
            missions: list = list(get_all_missions())
            endMissionQuery = datetime.now()

            time_diff: int = int((endMissionQuery - startMissionQuery).total_seconds() * 1000)
            print('Executed MongoDB in', time_diff, 'ms')

            for mission in missions:
                assets: list = mission['context']['assets']
                interval: int = mission['context']['interval']
                print('[ASSETS TO QUERY] :', assets)
                for asset in assets:
                    currency: str = 'EUR'
                    start_bot_analysis = datetime.now()
                    run_bot(asset=asset,
                            currency=currency,
                            interval=int(interval),
                            length_assets=len(mission['context']['assets']))
                    end_bot_analysis = datetime.now()
                    time_diff: int = int((end_bot_analysis - start_bot_analysis).total_seconds() * 1000)
                    print('Executed bot analysis in', time_diff, 'ms')

                time_to_sleep: float = interval * 10 * 2
                endPipeline = datetime.now()
                time_diff: int = int((endPipeline - startMissionQuery).total_seconds() * 1000)
                print('Executed full pipeline in', time_diff, 'ms')

                print('Sleeping for about', time_to_sleep, 'seconds.')
                sleep(time_to_sleep)

        except pymongo.errors.ServerSelectionTimeoutError:
            nbr_mongo_try = nbr_mongo_try + 1
            if nbr_mongo_try > 5:
                raise UnableToConnectMongoDBInstanceException("Try to connect Mongo instance multiple times "
                                                              "but unable to make a connection")
            sleep(10)


def start_multiprocess_bot():
    try:
        t1 = Process(target=bot_main_process)
        t2 = Process(target=bot_realtime_child_process)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    except Exception as err:
        print('[EXCEPTION] - CORE - sending email', err)
        send_email('Exception', str(err), {})
        raise err


if __name__ == "__main__":
    start_multiprocess_bot()
