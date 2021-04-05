import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from peakdetect import peakdetect

from kraken_trade_service import getCurrentBalance


class TrendAnalyzer:
    def __init__(self, df, asset, currency):
        self.df = df
        self.asset = asset
        self.currency = currency
        self.analyse_trends()
        self.make_decision()

    def analyse_trends(self):
        print('\n[TREND ANALYSIS]')

        macd_high, macd_low, self.pathFigMACD = find_multiple_curve_min_max(self.df, 'macds')
        close_high, close_low, self.pathFigCLOSE = find_multiple_curve_min_max(self.df, 'close_12_ema')

        self.index_size = len(self.df)
        self.last_macd_high, self.last_macd_low = get_last_index(macd_high, macd_low)
        self.last_close_high, self.last_close_low = get_last_index(close_high, close_low)

        print('\n[DETECTED LAST INDEX]', self.index_size)

        print('macd last index', self.last_macd_high, self.last_macd_low)
        print('close last index', self.last_close_high, self.last_close_low)

    def make_decision(self):
        print('\n[DECISION MAKING]')
        volume_to_buy = None

        DTO = {}
        # build_DTO(short_df, ['close'], index_size-1)

        attachments = [self.pathFigCLOSE, self.pathFigMACD]
        # send_email('[BOT-ANALYSIS]', 'Incoming analysis :D', attachments) # TODO - send emails
        for file in attachments:
            removeTmpPics(file)

        measure_to_store = ['close']
        stockAnalysis = {
            'close': self.df['close'][self.index_size - 1],
            'quantity': 1.
        }
        print(stockAnalysis)
        # stockAnalysis = build_DTO(short_df, measure_to_store, index_size-1)

        if self.last_close_low <= self.index_size - 5 or self.last_macd_low <= self.index_size - 5:
            print('BUY')
            volume_to_buy = define_quantity_volume(self.df, self.asset, self.currency)
        elif self.last_close_high <= self.index_size - 5 or self.last_macd_high <= self.index_size - 5:
            print('SELL')
            volume_to_buy = define_quantity_volume(self.df, self.asset, self.currency)

        print('volume to buy', volume_to_buy)


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
