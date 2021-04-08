import numpy as np
from peakdetect import peakdetect

from src.enginer_helper import plot_peaks_close_ema, define_quantity_volume, \
    remove_tmp_pics, get_last_index
from src.email_sender_helper import send_email
from src.timeseries_service import getLastEventByTypeAndAsset, addEvent


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

        try:
            if self.last_close_low <= self.index_size - 5 or self.last_macd_low <= self.index_size - 5:
                typeOfTrade = 'buy'

                previous_currency_trade = getLastEventByTypeAndAsset(self.asset, typeOfTrade)
                print('previous trade', previous_currency_trade)

                if not previous_currency_trade:
                    volume_to_buy = define_quantity_volume(self.df, typeOfTrade,
                                                           self.asset, self.currency,
                                                           self.length_assets, self.index_size - 1)
                    if volume_to_buy:
                        addEvent(typeOfTrade, volume_to_buy,
                                  self.df, self.index_size - 1)
                        send_email('[BOT-ANALYSIS]', 'Incoming trade : ' + typeOfTrade, attachments)
                        print('BUY this', volume_to_buy)

            elif self.last_close_high <= self.index_size - 5 or self.last_macd_high <= self.index_size - 5:
                typeOfTrade = 'sell'

                previous_currency_trade = getLastEventByTypeAndAsset(self.asset, typeOfTrade)
                print('previous trade', previous_currency_trade)

                volume_to_buy = define_quantity_volume(self.df, typeOfTrade,
                                                       self.asset, self.currency,
                                                       self.length_assets, self.index_size - 1)
                if volume_to_buy:
                    addEvent(typeOfTrade, volume_to_buy,
                             self.df, self.index_size - 1)
                    send_email('[BOT-ANALYSIS]', 'Incoming trade : ' + typeOfTrade, attachments)
                    print('SELL this', volume_to_buy)

        except Exception as err:
            send_email('Exception', str(err), {})

        print('[END OF ANALYSIS] ->', self.asset)
        print('\nResume to next asset')


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
