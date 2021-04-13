from datetime import datetime
from time import sleep

import matplotlib.pyplot as plt
import pymongo.errors

from src.services.krakenDataService import getFormattedData, get_stocks_indicators
from src.repository.missionRepository import getAllMissions
from src.engine.trendAnalyzer import TrendAnalyzer


def get_measure_viz(df, measure):
    df[measure].plot()
    plt.title(measure)
    plt.show()


def get_last_n_percentage(df, nbr_percentage):
    calculated_length = (len(df) * nbr_percentage) / 100
    tmp_df = df[:int(calculated_length)]
    print('TMP_DF - from', datetime.fromtimestamp(tmp_df.head(1)['timestamp'].iloc[0]),
          'to', datetime.fromtimestamp(tmp_df.tail(1)['timestamp'].iloc[-1]))
    return tmp_df


def run_bot(asset, currency, interval, length_assets):
    df = getFormattedData(asset + currency, str(interval))
    df_with_indicators = get_stocks_indicators(df)

    three_day_DF = get_last_n_percentage(df_with_indicators, 35)
    TrendAnalyzer(three_day_DF, asset, currency, length_assets, interval)

    sleep_between_analysis = interval / 10
    print('Sleeping for about', sleep_between_analysis, 'seconds.')
    sleep(sleep_between_analysis)


if __name__ == "__main__":
    print("[TRADING BOT]\n")
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
        except pymongo.errors.ServerSelectionTimeoutError:
            sleep(30)
