import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from peakdetect import peakdetect

from src.services.krakenTradeService import getAccountBalance


class NothingToTrade(Exception): pass


def define_volume(df, type_of_trade, nbr_asset_on_trade, index_max):
    print('\n[VOLUME TRADING QUANTITY]')
    print('Type of trade:', type_of_trade)

    volume_to_buy = None
    try:
        balance_euro = float(getAccountBalance()['result']['ZEUR'])
        maximum_percentage = .9
        money_available = (balance_euro / float(nbr_asset_on_trade)) * maximum_percentage
        volume_to_buy = money_available / df['close'][index_max]

    except Exception as err:
        raise err

    return volume_to_buy


def plot_peaks_close_ema(df, key, higher_peaks, lower_peaks):
    fig = plt.figure()
    plt.ion()
    plt.title(key)
    plt.plot(df[key])
    if key == 'close_12_ema':
        plt.plot(df['close'])

    plt.plot(higher_peaks[:, 0], higher_peaks[:, 1], 'ro')
    plt.plot(lower_peaks[:, 0], lower_peaks[:, 1], 'go')

    path_to_save_figure = '/tmp/' + str(datetime.now()) + '-' + key + '.png'
    plt.savefig(path_to_save_figure)
    plt.close('all')
    return path_to_save_figure


def build_DTO(df, measures, index):
    DTO = {}
    for measure in measures:
        DTO[measure] = df[measure][index]
    return DTO


def remove_tmp_pics(path):
    try:
        os.remove(path)
        print('Removed tmp plot figure from', path)
    except OSError:
        pass


def get_last_index(peaks_high, peaks_low):
    last_high_index = peaks_high[:, 0][len(peaks_high[:, 1]) - 1]
    last_low_index = peaks_low[:, 0][len(peaks_low[:, 1]) - 1]
    return last_high_index, last_low_index


def find_multiple_curve_min_max(df, key):
    print('CURVE - ', key, '- Detecting peaks min/max')
    length_df = len(df)
    if df[key][length_df - 1] > 0:
        print('POSITIVE')
    else:
        print('NEGATIVE')

    peaks = peakdetect(df[key], lookahead=2)
    higher_peaks = np.array(peaks[0])
    lower_peaks = np.array(peaks[1])

    path_fig = plot_peaks_close_ema(df, key, higher_peaks, lower_peaks)
    return higher_peaks, lower_peaks, path_fig
