import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from peakdetect import peakdetect

from src.services.krakenTradeService import getAccountBalance
from src.services.timeseriesService import getLastEventByTypeAndAsset
from src.services.timeseriesService import getTransaction


class NothingToTrade(Exception): pass


def define_volume(df, type_of_trade, asset, currency, nbr_asset_on_trade, index_max):
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


def calculate_volume_to_buy(self, type_of_trade):

    if type_of_trade == 'buy':
        previous_currency_trade = getLastEventByTypeAndAsset(self.asset, type_of_trade)
        # Ignore the previous trade if it has been fullfilled
        if previous_currency_trade:
            transaction = getTransaction(previous_currency_trade['fields']['transactionId'])
            try:
                if transaction['sell']:
                    previous_currency_trade = None
            except KeyError:
                pass

        # If there is no previous trade, define quantity
        if not previous_currency_trade:
            volume = define_volume(df=self.df,
                                   type_of_trade=type_of_trade,
                                   asset=self.asset,
                                   currency=self.currency,
                                   nbr_asset_on_trade=self.length_assets,
                                   index_max=self.index_size - 1)
            return volume, None

    if type_of_trade == 'sell':
        previous_currency_trade = getLastEventByTypeAndAsset(self.asset, 'buy')
        if previous_currency_trade:
            transaction_id = previous_currency_trade['transactionId']
            transaction = getTransaction(transaction_id)
            return transaction['buy']['fields']['quantity'], transaction_id

    return None, None


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

    path_fig = plot_peaks_close_ema(df, key, higher_peaks, lower_peaks)
    return higher_peaks, lower_peaks, path_fig
