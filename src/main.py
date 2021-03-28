from datetime import datetime

import matplotlib.pyplot as plt

from data_acquisition import getFormattedData
from stocks_indicators import get_stocks_indicators


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
    print(df['macds'][len(df)-1])
    for n in range(len(df) - 1, 0, -1):
        first_index = None
        if df['macds'][n] > df['macds'][n - 1]:
            if first_index is None:
                first_index = n
            last_index = n
            if last_index > first_index - 5:
                print('Found 5 concurrent value')
                timestamp = str(datetime.fromtimestamp(df['timestamp'][last_index]))
                price = df['close_26_ema'][last_index]

                tendency[first_index] = {"top": {"datetime": timestamp, "price": price}}
                print(tendency)
            return first_index

    print('TODO - Understand trend while curve is currently going up')


def high_volatility_volume_analysis(df, short_df):
    print('\n[TREND ANALYSIS]')
    tendency = detect_top_bottom(short_df)
    print(tendency)


if __name__ == "__main__":
    asset = 'GRTEUR'
    interval = '60'
    df = getFormattedData(asset, interval)
    df_with_indicators = get_stocks_indicators(df)
    three_day_DF = get_last_n_percentage(df_with_indicators, 25)

    # get_measure_viz(tmp_df, 'close_12_ema')
    get_measure_viz(three_day_DF, 'close_26_ema')
    get_measure_viz(three_day_DF, 'macds')
    # get_measure_viz(tmp_df, 'macd')
    # get_measure_viz(tmp_df, 'macdh')

    high_volatility_volume_analysis(df_with_indicators, three_day_DF)
