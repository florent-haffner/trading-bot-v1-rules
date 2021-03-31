import numpy as np
import matplotlib.pyplot as plt
from peakdetect import peakdetect


def trend_analysis(df, short_df):
    print('\n[TREND ANALYSIS]')

    find_multiple_curve_min_max(short_df, 'macds')
    find_multiple_curve_min_max(short_df, 'close_12_ema')
    plot_close_ema(df)


def plot_peaks_close_ema(df, key, higher_peaks, lower_peaks):
    plt.plot(df[key])
    plt.plot(higher_peaks[:, 0], higher_peaks[:, 1], 'ro')
    plt.plot(lower_peaks[:, 0], lower_peaks[:, 1], 'ko')
    plt.show()

def plot_close_ema(df):
    plt.plot(df['close'])
    plt.plot(df['close'], 'r')
    plt.show()



def find_multiple_curve_min_max(df, key):
    print('CURVE - Detecting peaks min/max')

    length_df = len(df)
    print('nbr of data', length_df)
    if df['macds'][length_df - 1] > 0:
        # TODO # Check the last 5 points and detect a brutal up/down
        print('VOLUME - POSITIVE')
    else:
        # TODO # Check the last 5 points and detect a brutal up/down
        print('VOLUME - NEGATIVE')

    print(df.describe()[key])
    peaks = peakdetect(df[key], lookahead=4)
    higher_peaks = np.array(peaks[0])
    lower_peaks = np.array(peaks[1])

    plot_peaks_close_ema(df, key, higher_peaks, lower_peaks)
    return higher_peaks, lower_peaks
