from datetime import datetime

import matplotlib.pyplot as plt

from data_acquisition import getFormattedData
from stocks_indicators import get_stocks_indicators

__HOURS_BEFORE_TREND_CHANGE = 10

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


def detect_top_bottom(df):
    print('CURVE - Detecting tendancy')
    tendency = {}
    if df['macds'][len(df)-1] > 0:
        print('VOLUME - UP')
    else: print('VOLUME - down')

    for n in range(len(df) - 1, 0, -1):
        top_index = None
        bottom_index = None
        if df['macds'][n] > df['macds'][n - 1]:
            if top_index is None:
                top_index = n
            last_index = n
            if last_index > top_index - __HOURS_BEFORE_TREND_CHANGE:
                print('TOP CURVE - Found', __HOURS_BEFORE_TREND_CHANGE, 'concurrent value')
                timestamp = str(datetime.fromtimestamp(df['timestamp'][last_index]))
                price = df['close_26_ema'][last_index]

                tendency[top_index] = {"top": {"datetime": timestamp, "price": price}}

    return tendency

    print('TODO - Understand trend while curve is currently going up')


def trend_analysis(df, short_df):
    print('\n[TREND ANALYSIS]')
    tendency = detect_top_bottom(short_df)
    print(tendency)


if __name__ == "__main__":
    asset = 'GRTEUR'
    interval = '60'
    df = getFormattedData(asset, interval)
    df_with_indicators = get_stocks_indicators(df)
    three_day_DF = get_last_n_percentage(df_with_indicators, 35)

    # get_measure_viz(three_day_DF, 'close')
    get_measure_viz(three_day_DF, 'close_12_ema')
    # get_measure_viz(three_day_DF, 'close_26_ema')
    get_measure_viz(three_day_DF, 'macds')
    # get_measure_viz(tmp_df, 'macd')
    # get_measure_viz(tmp_df, 'macdh')

    trend_analysis(df_with_indicators, three_day_DF)
