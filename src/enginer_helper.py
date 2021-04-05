import os
from datetime import datetime
import matplotlib.pyplot as plt

from src.kraken_trade_service import getCurrentBalance


def define_quantity_volume(df, asset, currency):
    print('[VOLUME TRADING QUANTITY]')
    # TODO -> check on InfluxDB if already possess currency
    balance = getCurrentBalance(asset)
    print(balance)


def plot_peaks_close_ema(df, key, higher_peaks, lower_peaks):
    plt.title(key)
    plt.plot(df[key])
    plt.plot(df['close'])
    plt.plot(higher_peaks[:, 0], higher_peaks[:, 1], 'ro')
    plt.plot(lower_peaks[:, 0], lower_peaks[:, 1], 'go')
    pathToSaveFigure = '/tmp/' + str(datetime.now()) + '-' + key + '.png'
    # print(pathToSave)
    plt.savefig(pathToSaveFigure)
    plt.show()
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


def removeTmpPics(path):
    os.remove(path)
    print('Removed tmp plot figure from', path)


def get_last_index(peaks_high, peaks_low):
    last_high_index = peaks_high[:, 0][len(peaks_high[:, 1]) - 1]
    last_low_index = peaks_low[:, 0][len(peaks_low[:, 1]) - 1]
    return last_high_index, last_low_index
