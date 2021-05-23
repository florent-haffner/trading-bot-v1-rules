from datetime import datetime
from typing import List

import numpy as np
import pandas as pd
from numpy import mean
from peakdetect import peakdetect

from src.engine.analysisEngineHelper import define_volume
from src.helpers.emailSenderHelper import send_email
from src.services.tradeEventService import add_trade_event, get_last_trade_event_by_type_and_asset
from src.services.transactionService import get_transaction


# TODO -> type this
def compute_mean_peaks(df: pd.DataFrame, margin: int):
    peaks = peakdetect(df['close'], lookahead=margin)
    higher_peaks = np.array(peaks[0])
    lower_peaks = np.array(peaks[1])

    last_event = df['close'][len(df) - 1]
    high_mean: float = float(mean(higher_peaks[:, 1]))
    low_mean: float = float(mean(lower_peaks[:, 1]))
    return high_mean, low_mean, higher_peaks, lower_peaks, last_event


class AnalysisEngine:
    def __init__(self, debug: bool, df: pd.DataFrame, asset: str, currency: str, length_assets: int, interval: int):
        self.df: pd.DataFrame = df
        self.debug: bool = debug
        self.asset: str = asset
        self.currency: str = currency
        self.length_assets: int = length_assets
        self.interval: int = interval
        self.event_type: str = ''
        self.index_size: int = len(self.df)

        self.detect_short_time_trend()
        self.make_decision()

    def detect_short_time_trend(self):
        print(self.asset, '- Short time detection')

        tree_hour_in_minute: int = 60 * 3
        shorter_df: pd.DataFrame = self.df[tree_hour_in_minute:]
        shorter_df.reset_index(inplace=True)
        print('SHORT TIME DF - first:', datetime.fromtimestamp(shorter_df.head(1)['timestamp'].iloc[0]),
              'last:', datetime.fromtimestamp(shorter_df.tail(1)['timestamp'].iloc[-1]))

        high_mean_short, low_mean_short, higher_peaks_short, lower_peaks_short, last_close = \
            compute_mean_peaks(shorter_df, 1)
        print('last', round(last_close, 4),
              'high_mean', round(high_mean_short, 4),
              'low_mean', round(low_mean_short, 4))

        one_hour: int = 60
        last_hour_df: pd.DataFrame = shorter_df[one_hour:]
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
        attachments: List = []
        try:
            print('Type of trade:', self.event_type)
            if self.event_type == 'buy':
                self.generate_trade_event(self.event_type, attachments=attachments)

            elif self.event_type == 'sell':
                self.generate_trade_event(self.event_type, attachments=attachments)

            else:
                print('Trends are currently evolving, waiting...')

        except Exception as err:
            print('[EXCEPTION] - sending email', err)
            send_email('Exception', str(err), {})
            if self.debug:
                raise err

        print('\n[END OF ANALYSIS] ->', self.asset)
        print('\nResume to follow next action', '\n------------------\n')

    def generate_trade_event(self, type_of_trade: str, attachments: List):
        print('Calculating volume')
        volume_to_buy: float
        transaction_id: str
        volume_to_buy, transaction_id = self.calculate_volume_to_buy(type_of_trade)
        if volume_to_buy:
            success = add_trade_event(type_of_trade=type_of_trade,
                                      volume_to_buy=volume_to_buy,
                                      asset=self.asset,
                                      interval=self.interval,
                                      currency=self.currency,
                                      transaction_id=transaction_id)
            if success:
                print(type_of_trade.upper(), 'this', volume_to_buy, 'of', self.asset)
        else:
            print('Nothing to', type_of_trade)

    def calculate_volume_to_buy(self, type_of_trade: str) -> (float, str):
        if type_of_trade == 'buy':
            previous_currency_trade = get_last_trade_event_by_type_and_asset(self.asset, type_of_trade)
            print(self)
            # Ignore the previous trade if it has been fulfilled
            if previous_currency_trade:
                transaction = get_transaction(previous_currency_trade['transactionId'])
                try:
                    if transaction['sell']:
                        previous_currency_trade = None
                except KeyError:
                    pass

            # If there is no previous trade, define quantity
            if not previous_currency_trade:
                volume: float = define_volume(df=self.df,
                                              type_of_trade=type_of_trade,
                                              nbr_asset_on_trade=self.length_assets,
                                              index_max=self.index_size - 1)
                return volume, None

        if type_of_trade == 'sell':
            previous_currency_trade = get_last_trade_event_by_type_and_asset(self.asset, 'buy')
            if previous_currency_trade:
                transaction_id: str = previous_currency_trade['transactionId']
                transaction = get_transaction(transaction_id)
                return transaction['buy']['fields']['quantity'], transaction_id

        return None, None
