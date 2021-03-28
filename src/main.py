from datetime import datetime

import matplotlib.pyplot as plt

from data_acquisition import getFormattedData
from engine import trend_analysis
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
