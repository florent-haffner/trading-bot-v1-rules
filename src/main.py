from datetime import datetime

import matplotlib.pyplot as plt

from kraken_data_service import getFormattedData
from mission_service import getAllMissions
from engine import TrendAnalyzer
from stocks_indicators_helper import get_stocks_indicators


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
    TrendAnalyzer(three_day_DF, asset, currency, length_assets)


if __name__ == "__main__":
    print("[TRADING BOT]\n")
    missions = list(getAllMissions())

    for mission in missions:
        assets = mission['context']['assets']
        print('[ASSETS TO QUERY] :', assets)
        for asset in assets:
            currency = 'EUR'
            interval = mission['context']['interval']
            run_bot(asset, currency, interval, len(assets))
            # TODO - wait 15s
