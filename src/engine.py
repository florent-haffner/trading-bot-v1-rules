import numpy as np
import matplotlib.pyplot as plt
from peakdetect import peakdetect


def trend_analysis(df, short_df):
    print('\n[TREND ANALYSIS]')

    find_multiple_curve_min_max(short_df, 'macds')
    find_multiple_curve_min_max(short_df, 'close_26_ema')


def find_multiple_curve_min_max(df, key):
    print('CURVE - Detecting tendancy')

    length_df = len(df)
    print('nbr of data', length_df)
    if df['macds'][length_df - 1] > 0:
        # TODO # Check the last 5 points and detect a brutal up/down
        print('VOLUME - POSITIVE')
    else:
        # TODO # Check the last 5 points and detect a brutal up/down
        print('VOLUME - NEGATIVE')

    print(df.describe()[key])
    peaks = peakdetect(df[key], lookahead=8)
    higher_peaks = np.array(peaks[0])
    lower_peaks = np.array(peaks[1])

    plt.plot(df[key])
    plt.plot(higher_peaks[:, 0], higher_peaks[:, 1], 'ro')
    plt.plot(lower_peaks[:, 0], lower_peaks[:, 1], 'ko')
    plt.show()

    return higher_peaks, lower_peaks
