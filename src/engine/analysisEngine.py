from datetime import datetime

import numpy as np
import pandas as pd
from numpy import mean
from peakdetect import peakdetect

from src.engine.analysisEngineHelper import get_last_index, find_multiple_curve_min_max, define_volume
from src.helpers.dateHelper import DATE_STR
from src.helpers.emailSenderHelper import send_email
from src.services.timeseriesService import addTradeEvent, getLastEventByTypeAndAsset, getTransaction


def compute_mean_peaks(df: pd.DataFrame, margin: int):
    peaks = peakdetect(df['close'], lookahead=margin)
    higher_peaks = np.array(peaks[0])
    lower_peaks = np.array(peaks[1])

    last_event = df['close'][len(df) - 1]
    high_mean: float = float(mean(higher_peaks[:, 1]))
    low_mean: float = float(mean(lower_peaks[:, 1]))
    return high_mean, low_mean, higher_peaks, lower_peaks, last_event


class AnalysisEngine:
    def __init__(self, mode, df, asset, currency, length_assets, interval):
        self.df = df
        self.debug = mode
        self.asset = asset
        self.currency = currency
        self.length_assets = length_assets
        self.interval = interval
        self.event_type = None
        self.index_size = None

        self.analyse_trends()
        self.make_decision()

    def analyse_trends(self):
        print('\n[TREND ANALYSIS]')

        # nbr_occurrences = 4
        # macd_high, macd_low, self.pathFigMACD = find_multiple_curve_min_max(self.df,
        #                                                                     key='macds',
        #                                                                     nbr_occurrences=nbr_occurrences)
        # close_high, close_low, self.pathFigClose = find_multiple_curve_min_max(self.df,
        #                                                                        key='close',
        #                                                                        nbr_occurrences=nbr_occurrences)

        self.index_size = len(self.df)
        self.detect_short_time_trend()

    def detect_short_time_trend(self):
        print(self.asset, '- Short time detection')

        tree_hour_in_minute = 60 * 3
        shorter_df = self.df[tree_hour_in_minute:]
        shorter_df.reset_index(inplace=True)
        print('SHORT TIME DF - first:', datetime.fromtimestamp(shorter_df.head(1)['timestamp'].iloc[0]),
              'last:', datetime.fromtimestamp(shorter_df.tail(1)['timestamp'].iloc[-1]))

        high_mean_short, low_mean_short, higher_peaks_short, lower_peaks_short, last_close = \
            compute_mean_peaks(shorter_df, 1)
        print('last', round(last_close, 4),
              'high_mean', round(high_mean_short, 4),
              'low_mean', round(low_mean_short, 4))

        one_hour = 60
        last_hour_df = shorter_df[one_hour:]
        last_hour_df.reset_index(inplace=True)

        high_mean_shorter, low_mean_shorter, higher_peaks_shorter, lower_peaks_shorter, _ = \
            compute_mean_peaks(last_hour_df, 1)
        print('last', round(last_close, 4),
              'high_mean', round(high_mean_shorter, 4),
              'low_mean', round(low_mean_shorter, 4))

        if last_close < low_mean_short:
            self.event_type = 'buy'
        elif last_close > low_mean_short:
            self.event_type = 'sell'
        else:
            self.event_type = 'wait'

    def make_decision(self):
        print('\n[DECISION MAKING]')
        # attachments = [self.pathFigClose]
        attachments = None
        try:
            print('Type of trade:', self.event_type)
            if self.event_type == 'buy':
                self.generate_trade_event(self.event_type, attachments=attachments)

            elif self.event_type == 'sell':
                self.generate_trade_event(self.event_type, attachments=attachments)

            else:
                print('Trends are currently evolving, waiting...')

        except Exception as err:
            if self.debug:
                raise err
            print('[EXCEPTION] - sending email', err)
            send_email('Exception', str(err), {})

        print('\n[END OF ANALYSIS] ->', self.asset)
        print('\nResume to follow next action', '\n------------------\n')

    def generate_trade_event(self, type_of_trade, attachments):
        print('Calculating volume')
        volume_to_buy, transaction_id = self.calculate_volume_to_buy(type_of_trade)
        if volume_to_buy:
            success = addTradeEvent(type_of_trade=type_of_trade,
                                    volume_to_buy=volume_to_buy,
                                    asset=self.asset,
                                    interval=self.interval,
                                    currency=self.currency,
                                    transaction_id=transaction_id)
            if success:
                # send_email(
                #     '[BOT-ANALYSIS]', 'Incoming trade : [' + self.asset + '] - type: ' + type_of_trade,
                #     attachments)
                print(type_of_trade.upper(), 'this', volume_to_buy, 'of', self.asset)
        else:
            print('Nothing to', type_of_trade)

    def calculate_volume_to_buy(self, type_of_trade):
        if type_of_trade == 'buy':
            previous_currency_trade = getLastEventByTypeAndAsset(self.asset, type_of_trade)
            # Ignore the previous trade if it has been fullfilled
            if previous_currency_trade:
                transaction = getTransaction(previous_currency_trade['transactionId'])
                try:
                    if transaction['sell']:
                        previous_currency_trade = None
                except KeyError:
                    pass

            # If there is no previous trade, define quantity
            if not previous_currency_trade:
                volume = define_volume(df=self.df,
                                       type_of_trade=type_of_trade,
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

