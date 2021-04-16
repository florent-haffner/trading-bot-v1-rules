import os
from datetime import datetime
from time import sleep

import pymongo.errors
import pandas as pd

from src.engine.trendAnalyzer import TrendAnalyzer
from src.repository.missionRepository import getAllMissions
from src.services.krakenDataService import getFormattedData, get_stocks_indicators

__DEBUG = True


def get_last_n_percentage(df, nbr_percentage):
    calculated_length = (len(df) * nbr_percentage) / 100
    tmp_df = df[:int(calculated_length)]
    print('TMP_DF - from', datetime.fromtimestamp(tmp_df.head(1)['timestamp'].iloc[0]),
          'to', datetime.fromtimestamp(tmp_df.tail(1)['timestamp'].iloc[-1]))
    return tmp_df


def run_bot(asset, currency, interval, length_assets):
    df = None
    if not __DEBUG:
        print('DEVELOPMENT MODE')
        df = getFormattedData(asset + currency, str(interval))
    else:
        print('SIMULATION MODE')
        type_of_trade = ['buy', 'sell']
        chosen_type = type_of_trade[0]
        path_csv = os.getcwd() + '/data/mock-' + asset + '-' + chosen_type + '.csv'
        print('Get CSV from ', path_csv)
        df = pd.read_csv(path_csv)

    df_with_indicators = get_stocks_indicators(df)

    three_day_DF = get_last_n_percentage(df_with_indicators, 35)
    TrendAnalyzer(__DEBUG, three_day_DF, asset, currency, length_assets, interval)

    sleep_between_analysis = interval / 10
    print('Sleeping for about', sleep_between_analysis, 'seconds.')
    sleep(sleep_between_analysis)


def run():
    print("[TRADING BOT]\n")
    # sleep(10)
    while True:
        try:
            missions = list(getAllMissions())
            for mission in missions:
                assets = mission['context']['assets']
                interval = mission['context']['interval']
                print('[ASSETS TO QUERY] :', assets)
                for asset in assets:
                    currency = 'EUR'
                    run_bot(asset, currency, interval, len(assets))

                # time_to_sleep = (interval * 60) / 8
                print('Sleeping for about', interval, 'seconds.')
                sleep(interval)

                if __DEBUG:
                    print('\n[DEBUG = ON] -> Shutting down the bot')
                    break
            if __DEBUG: break

        except pymongo.errors.ServerSelectionTimeoutError:
            sleep(30)


if __name__ == "__main__":
    run()
