from datetime import datetime

import matplotlib.pyplot as plt

from kraken_data_service import getFormattedData
from email_sender_helper import  get_cowsay_asci
from engine import trend_analysis
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


def run_bot(asset, interval):
    df = getFormattedData(asset, interval)
    df_with_indicators = get_stocks_indicators(df)

    three_day_DF = get_last_n_percentage(df_with_indicators, 35)
    trend_analysis(df_with_indicators, three_day_DF)


if __name__ == "__main__":
    print(get_cowsay_asci("Hello you ! :D"))
    # while True:
    asset = 'GRTEUR'
    interval = '60'
    run_bot(asset, interval)
