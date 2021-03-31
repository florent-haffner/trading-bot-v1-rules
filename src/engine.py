import numpy as np
import matplotlib.pyplot as plt
from peakdetect import peakdetect


def trend_analysis(df, short_df):
    print('\n[TREND ANALYSIS]')

    macd_high, macd_low = find_multiple_curve_min_max(short_df, 'macds')
    close_high, close_low = find_multiple_curve_min_max(short_df, 'close_12_ema')
    # plot_close_ema(df)

    size_data = len(short_df)

    last_macd_high, last_macd_low = get_last_index(macd_high, macd_low)
    last_close_high, last_close_low = get_last_index(close_high, close_low)

    print('\n[DETECTED LAST INDEX]', size_data)

    print('macd last index', last_macd_high, last_macd_low)
    print('close last index', last_close_high, last_close_low)

    print('\n[DECISION]')
    if last_macd_high <= size_data <= last_macd_high or last_close_high <= size_data:
        print('SELL')
    elif last_macd_low <= size_data or last_close_low <= size_data:
        print('BUY')


def plot_peaks_close_ema(df, key, higher_peaks, lower_peaks):
    plt.title(key)
    plt.plot(df[key])
    plt.plot(higher_peaks[:, 0], higher_peaks[:, 1], 'ro')
    plt.plot(lower_peaks[:, 0], lower_peaks[:, 1], 'ko')
    plt.show()


def plot_close_ema(df):
    plt.title('MM')
    plt.plot(df['close'])
    plt.plot(df['dx_6_ema'], 'r')
    plt.show()


def find_multiple_curve_min_max(df, key):
    print('CURVE - ', key, '- Detecting peaks min/max')

    length_df = len(df)
    if df[key][length_df - 1] > 0:
        print('POSITIVE')
    else:
        print('NEGATIVE')

    peaks = peakdetect(df[key], lookahead=4)
    higher_peaks = np.array(peaks[0])
    lower_peaks = np.array(peaks[1])

    plot_peaks_close_ema(df, key, higher_peaks, lower_peaks)
    return higher_peaks, lower_peaks


def get_last_index(peaks_high, peaks_low):
    last_high_index = peaks_high[:, 0][len(peaks_high[:, 1]) - 1]
    last_low_index = peaks_low[:, 0][len(peaks_low[:, 1]) - 1]
    return last_high_index, last_low_index
