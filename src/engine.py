from scipy.signal import find_peaks


def trend_analysis(df, short_df):
    print('\n[TREND ANALYSIS]')
    find_multiple_curve_min_max(short_df, 'macds')


def find_multiple_curve_min_max(df, key):
    print('CURVE - Detecting tendancy')
    length_df = len(df)
    print('nbr of data', length_df)
    if df['macds'][length_df - 1] > 0:
        print('VOLUME - UP')
    else:
        print('VOLUME - down')

    peaks_maximum = find_peaks(df[key], height=0.002)
    peaks_minimum = find_peaks(-df[key], height=0.002)
    print(list(peaks_minimum[0]), list(peaks_maximum[0]))
    return None
