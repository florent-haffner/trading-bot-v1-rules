import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from peakdetect import peakdetect

from src.services.krakenTradeService import getAccountBalance
from src.services.timeseriesService import getLastEventByTypeAndAsset


class NothingToTrade(Exception): pass


def define_quantity_volume(df, type_of_trade, asset, currency, nbr_asset_on_trade, index_max):
    print('\n[VOLUME TRADING QUANTITY]')
    print('Type of trade:', type_of_trade)

    volume_to_buy = None
    try:
        balanceEuro = float(getAccountBalance()['result']['ZEUR'])
        maximumPercentage = .9
        money_available = (balanceEuro / float(nbr_asset_on_trade)) * maximumPercentage
        volume_to_buy = money_available * df['close'][index_max]

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

    pathToSaveFigure = '/tmp/' + str(datetime.now()) + '-' + key + '.png'

    plt.savefig(pathToSaveFigure)
    plt.close('all')
    return pathToSaveFigure


def plot_close_ema(df):
    plt.title('MM')
    plt.plot(df['close'])
    plt.plot(df['dx_6_ema'], 'r')
    plt.show()


def build_DTO(df, measures, index):
    DTO = {}
    for measure in measures:
        DTO[measure] = df[measure][index]
    return DTO


def remove_tmp_pics(path):
    try:
        os.remove(path)
        print('Removed tmp plot figure from', path)
    except Exception: pass


def get_last_index(peaks_high, peaks_low):
    last_high_index = peaks_high[:, 0][len(peaks_high[:, 1]) - 1]
    last_low_index = peaks_low[:, 0][len(peaks_low[:, 1]) - 1]
    return last_high_index, last_low_index


def calculate_volume_to_buy(self, typeOfTrade):
    previous_currency_trade = getLastEventByTypeAndAsset(self.asset, typeOfTrade)
    print('previous trade', previous_currency_trade)

    volume_to_buy = None
    if not previous_currency_trade:
        volume_to_buy = define_quantity_volume(df=self.df,
                                               type_of_trade=typeOfTrade,
                                               asset=self.asset,
                                               currency=self.currency,
                                               nbr_asset_on_trade=self.length_assets,
                                               index_max=self.index_size - 1)
    return volume_to_buy


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

    pathFig = plot_peaks_close_ema(df, key, higher_peaks, lower_peaks)
    return higher_peaks, lower_peaks, pathFig
