from datetime import datetime

import matplotlib.pyplot as plt

from data_acquisition import getFormattedData
from stocks_indicators import get_stocks_indicator


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


def detect_last_recent_top(df):
    print('Comparing current macds to previous one')
    for n in range(len(df) - 1, 0, -1):
        first_index = None
        top_index = None
        if (df['macds'][n] > df['macds'][n - 1]):
            if first_index is None:
                first_index = n
            top_index = n
            if top_index > first_index-5:
                print('Found 5 concurrent value - Curve to detected')
                print('Last recent top found at', datetime.fromtimestamp(df['timestamp'][top_index]))
            return first_index

        print('TODO - Understand trend while curve is currently going up')


def high_valatility_volume_analysis(df, short_df):
    print('\n[TREND ANALYSIS]')
    top_index = detect_last_recent_top(short_df)
    print(top_index)


if __name__ == "__main__":
    asset = 'GRTEUR'
    interval = '60'
    df = getFormattedData(asset, interval)

    df = get_stocks_indicator(df)
    tmp_df = get_last_n_percentage(df, 25)

    get_measure_viz(tmp_df, 'close_12_ema')
    get_measure_viz(tmp_df, 'close_26_ema')

    get_measure_viz(tmp_df, 'macd')
    get_measure_viz(tmp_df, 'macds')
    get_measure_viz(tmp_df, 'macdh')

    high_valatility_volume_analysis(df, tmp_df)
