import os
from datetime import datetime
import matplotlib.pyplot as plt

from src.kraken_trade_service import getAccountBalance, getTradeBalance
from src.timeseries_repository import getRecentEventByTypeAndAsset, getLastTradeEventByType


class NothingToTrade(Exception): pass


def define_quantity_volume(df, type_of_trade, asset, currency, nbr_asset_on_trade, index_max):
    print('[VOLUME TRADING QUANTITY]')
    print('Type of trade:', type_of_trade)

    # TODO -> check on InfluxDB if already possess currency
    previous_currency_trade = getLastTradeEventByType(type_of_trade)
    print(previous_currency_trade)
    volume_to_buy = None

    try:
        if not previous_currency_trade:
            balanceEuro = float(getAccountBalance()['result']['ZEUR'])
            maximumPercentage = .9
            volume_to_buy = (balanceEuro / float(nbr_asset_on_trade)) * maximumPercentage

        else:
            raise NothingToTrade('Something is already being trade')
    except Exception as err:
        raise err

    return volume_to_buy


def plot_peaks_close_ema(df, key, higher_peaks, lower_peaks):
    plt.title(key)
    plt.plot(df[key])
    plt.plot(df['close'])
    plt.plot(higher_peaks[:, 0], higher_peaks[:, 1], 'ro')
    plt.plot(lower_peaks[:, 0], lower_peaks[:, 1], 'go')

    pathToSaveFigure = '/tmp/' + str(datetime.now()) + '-' + key + '.png'
    plt.savefig(pathToSaveFigure)
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
