import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def trend_analysis(df, short_df):
    print('\n[TREND ANALYSIS]')

    print(df['macds'].describe())
    print(df['macds'].describe()['std'])
    find_multiple_curve_min_max(short_df, 'macds', 0.002, None)

    print(df['close_12_ema'].describe())
    print(df['close_12_ema'].describe()['std'])
    find_multiple_curve_min_max(short_df, 'close_12_ema', None, None)


def find_multiple_curve_min_max(df, key, height, distance):
    from peakdetect import peakdetect

    print('CURVE - Detecting tendancy')

    length_df = len(df)
    print('nbr of data', length_df)
    if df['macds'][length_df - 1] > 0:
        print('VOLUME - UP')
    else:
        print('VOLUME - down')


    print(df.describe()[key])
    peaks = peakdetect(df[key], lookahead=3)
    higher_peaks = np.array(peaks[0])
    lower_peaks = np.array(peaks[1])
    print(len(higher_peaks), len(lower_peaks))

    plt.plot(df[key])
    plt.plot(higher_peaks[:,0], higher_peaks[:,1], 'ro')
    plt.plot(lower_peaks[:,0], lower_peaks[:,1], 'ko')
    plt.show()


    peaks_maximum = find_peaks(df[key], height, distance)
    peaks_minimum = find_peaks(-df[key], height, distance)
    print('top', list(peaks_minimum[0]), 'bottom', list(peaks_maximum[0]))
    return None
