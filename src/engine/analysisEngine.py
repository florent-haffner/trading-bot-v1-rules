from datetime import datetime

from src.engine.analysisEngineHelper import get_last_index, find_multiple_curve_min_max, define_volume
from src.helpers.dateHelper import DATE_STR
from src.helpers.emailSenderHelper import send_email
from src.services.timeseriesService import addTradeEvent, getLastEventByTypeAndAsset, getTransaction


class AnalysisEngine:
    def __init__(self, mode, df, asset, currency, length_assets, interval):
        self.df = df
        self.debug = mode
        self.asset = asset
        self.currency = currency
        self.length_assets = length_assets
        self.interval = interval

        self.analyse_trends()
        self.make_decision()

    def analyse_trends(self):
        print('\n[TREND ANALYSIS]')

        nbr_occurrences = 4
        macd_high, macd_low, self.pathFigMACD = find_multiple_curve_min_max(self.df,
                                                                            key='macds',
                                                                            nbr_occurrences=nbr_occurrences)
        # close_12_high, close_12_low, self.pathFigCLOSE = find_multiple_curve_min_max(self.df,
        #                                                                              key='close_12_ema',
        #                                                                              nbr_occurrences=nbr_occurrences)
        close_high, close_low, self.pathFigClose = find_multiple_curve_min_max(self.df,
                                                                               key='close',
                                                                               nbr_occurrences=nbr_occurrences)

        self.index_size = len(self.df)
        self.last_macd_high, self.last_macd_low = get_last_index(macd_high, macd_low)
        # self.last_close_12_high, self.last_close_12_low = get_last_index(close_12_high, close_12_low)
        self.last_close_high, self.last_close_low = get_last_index(close_high, close_low)

        # # TODO -> REMOVE THIS
        # print(self.df)
        # print(self.df.keys())
        # import matplotlib.pyplot as plt
        # key = 'close'
        #
        # import numpy as np
        # from peakdetect import peakdetect
        #
        # peaks = peakdetect(self.df[key], lookahead=margin)
        # higher_peaks = np.array(peaks[0])
        # lower_peaks = np.array(peaks[1])
        #
        # plt.plot(self.df[key])
        # plt.plot(self.df['close_12_ema'])
        # plt.plot(higher_peaks[:, 0], higher_peaks[:, 1], 'ro')
        # plt.plot(lower_peaks[:, 0], lower_peaks[:, 1], 'go')
        #
        # print('higher_peaks', higher_peaks)
        # print('lower_peaks', lower_peaks)
        # plt.show()
        #
        # raise Exception('')

        print('\n[DETECTED LAST INDEX]', self.index_size)
        print('close index { high:', self.last_close_high, ' low:', self.last_close_low, '}')

    def make_decision(self):
        print('\n[DECISION MAKING]')
        attachments = [self.pathFigClose]
        try:
            margin_trade_out_of_range = 10
            if self.last_close_low >= self.index_size - margin_trade_out_of_range:
                type_of_trade = 'buy'
                print('Type of trade:', type_of_trade)
                self.compute_trade_event(type_of_trade, attachments=attachments)

            elif self.last_close_high >= self.index_size - margin_trade_out_of_range:
                type_of_trade = 'sell'
                print('Type of trade:', type_of_trade)
                self.compute_trade_event(type_of_trade, attachments=attachments)

            else:
                # TODO -> what about checking if I didn't already have stuff
                print('Trends are currently evolving, waiting...')

        except Exception as err:
            if self.debug:
                raise err
            print('[EXCEPTION] - sending email', err)
            send_email('Exception', str(err), {})

        print('\n[END OF ANALYSIS] ->', self.asset)
        print('\nResume to follow next action', '\n------------------\n')

    def compute_trade_event(self, type_of_trade, attachments):
        print('Calculating volume')
        date = datetime.now().strftime(DATE_STR)
        volume_to_buy, transaction_id = self.calculate_volume_to_buy(type_of_trade)

        if volume_to_buy:
            success = addTradeEvent(type_of_trade=type_of_trade,
                                    volume_to_buy=volume_to_buy,
                                    asset=self.asset,
                                    df=self.df,
                                    maximum_index=self.index_size - 1,
                                    interval=self.interval,
                                    date=date,
                                    transactionId=transaction_id)
            if success:
                send_email(
                    '[BOT-ANALYSIS]', 'Incoming trade : [' + self.asset + '] - type: ' + type_of_trade,
                    attachments)
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
