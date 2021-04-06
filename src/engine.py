import numpy as np
from datetime import datetime
from peakdetect import peakdetect

from src.enginer_helper import plot_peaks_close_ema, define_quantity_volume,\
    remove_tmp_pics, get_last_index, \
    NothingToTrade
from src.timeseries_repository import getRecentEventByType, getLastTradeEventByType


class TrendAnalyzer:
    def __init__(self, df, asset, currency, length_assets):
        self.df = df
        self.asset = asset
        self.currency = currency
        self.length_assets = length_assets
        self.__SERVER_HOST = '192.168.1.58'

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

        attachments = [self.pathFigCLOSE, self.pathFigMACD]
        # send_email('[BOT-ANALYSIS]', 'Incoming analysis :D', attachments) # TODO - send emails
        for file in attachments:
            remove_tmp_pics(file)

        try:
            if self.last_close_low <= self.index_size - 5 or self.last_macd_low <= self.index_size - 5:
                typeOfTrade = 'BUY'
                previous_currency_trade = getLastTradeEventByType(typeOfTrade)
                print(previous_currency_trade)

                # volume_to_buy = define_quantity_volume(self.df, typeOfTrade,
                #                                        self.asset, self.currency,
                #                                        self.length_assets, self.index_size - 1)
                if volume_to_buy:
                    DTO = generateDTO(self.__SERVER_HOST, typeOfTrade, volume_to_buy,
                                      self.df, self.index_size - 1)
                    getRecentEventByType([DTO])
                    print('BUY this', volume_to_buy)

            elif self.last_close_high <= self.index_size - 5 or self.last_macd_high <= self.index_size - 5:
                typeOfTrade = 'SELL'
                volume_to_buy = define_quantity_volume(self.df, typeOfTrade,
                                                       self.asset, self.currency,
                                                       self.length_assets, self.index_size - 1)
                print('TODO')  # TODO
        except NothingToTrade:
            print('There is nothing to trade')
            pass

        print('[END OF ANALYSIS] ->', self.asset)
        print('\nResume to next asset')


def generateDTO(host, type_of_trade, volume_to_buy, df, maximum_index):
    return {
        'measurement': 'tradeEvent',
        'time': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        'tags': {
            'typeOfTrade': type_of_trade,
        },
        'fields': {
            'quantity': volume_to_buy,
            'price': df['close'][maximum_index],
            'acknowledge': False
        }
    }


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
