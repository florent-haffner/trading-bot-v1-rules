from datetime import datetime
from multiprocessing import Process
from threading import Thread
from time import sleep

import pymongo.errors

from src.helpers.params import __DEBUG, __OFFLINE
from src.engine.analysisEngine import AnalysisEngine
from src.repository.missionRepository import getAllMissions
from src.services.krakenDataService import getFormattedData, get_stocks_indicators


def get_last_n_percentage(df, nbr_percentage):
    calculated_length = (len(df) * nbr_percentage) / 100
    tmp_df = df[int(calculated_length):]
    print('DF last -', nbr_percentage, '% - first:', datetime.fromtimestamp(tmp_df.head(1)['timestamp'].iloc[0]),
          'last:', datetime.fromtimestamp(tmp_df.tail(1)['timestamp'].iloc[-1]))
    return tmp_df


def run_bot(asset, currency, interval, length_assets):
    df = getFormattedData(asset + currency, str(interval))

    if __OFFLINE:
        import os
        import pandas as pd
        print('DEVELOPMENT MODE')
        type_of_trade = ['buy', 'sell']
        chosen_type = type_of_trade[0]
        path_csv = os.getcwd() + '/data/mock-' + asset + '-' + chosen_type + '.csv'
        print('Get CSV from ', path_csv)
        df = pd.read_csv(path_csv)

    df_with_indicators = get_stocks_indicators(df)
    print('DF FULL - first:', datetime.fromtimestamp(df_with_indicators.head(1)['timestamp'].iloc[0]),
          'last:', datetime.fromtimestamp(df_with_indicators.tail(1)['timestamp'].iloc[-1]))

    AnalysisEngine(__DEBUG, df_with_indicators, asset, currency, length_assets, interval)

    sleep_between_analysis = interval / 10
    print('Sleeping for about', sleep_between_analysis, 'seconds.')
    sleep(sleep_between_analysis)


def bot_main_process():
    print("[TRADING BOT]")
    if __DEBUG:
        print('SIMULATION MODE -> Exception will be raised\n')
    else:
        print('PRODUCTION MODE -> Exception will stay silent\n')
    sleep(1)

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

                time_to_sleep = interval * 10
                print('Sleeping for about', time_to_sleep, 'seconds.')
                sleep(time_to_sleep)

        except pymongo.errors.ServerSelectionTimeoutError:
            sleep(10)


def multiprocess():
    results = []  # Creating a Global Variable

    def calc_square(numbers):
        global results
        for i in numbers:
            print('square: ', str(i * i))
            results.append(i * i)
            print('witnin a result: ' + str(results))
    arr = [2, 3, 8, 9]
    p1 = Process(target=calc_square, args=(arr,))
    # creating one Process here p1
    p1.start()
    # starting Processes here parallel by using start function.
    p1.join()    # this join() will wait until the calc_square() function is    finished.
    print('result : '+str(results))  # this print didn't work here we have to print it within the process
    print("Successed!")


def multithread():
    def child_thread():
        while True:
            print("Child thread here")
            sleep(1)

    t1 = Thread(target=child_thread)
    t2 = Thread(target=bot_main_process)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    bot_main_process()

    # multithread()
    # multiprocess()  # Should be choose because I do I/O on network + calculation
