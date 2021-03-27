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


if __name__ == "__main__":
    asset = 'GRTEUR'
    interval = '60'
    df = getFormattedData(asset, interval)

    df = get_stocks_indicator(df)
    print(df.keys())

    tmp_df = get_last_n_percentage(df, 25)

    get_measure_viz(tmp_df, 'close_12_ema')
    get_measure_viz(tmp_df, 'close_26_ema')

    get_measure_viz(tmp_df, 'macd')
    get_measure_viz(tmp_df, 'macds')
    get_measure_viz(tmp_df, 'macdh')
