from datetime import datetime

import pandas as pd

from src.engine.analysisEngineHelper import define_quantity, compute_mean_peaks
from src.helpers.emailSenderHelper import send_email
from src.services.krakenPrivateTradeService import get_last_price
from src.services.telegramMessageService import send_message
from src.services.tradeEventService import add_trade_event, get_last_trade_event_by_type_and_asset
from src.services.transactionService import get_transaction


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
        self.decision_wrapper()

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

    def decision_wrapper(self):
        print('\n[DECISION MAKING]')
        try:
            print('Type of trade:', self.event_type)
            if self.event_type == 'buy':
                self.check_volume_to_buy_then_make_decision(self.event_type)

            elif self.event_type == 'sell':
                self.check_volume_to_buy_then_make_decision(self.event_type)
            else:
                print('Trends are currently evolving, waiting...')

        except Exception as err:
            print('[EXCEPTION] - ANALYSIS ENGINE - sending email', err)
            send_message('<p>Exception - ANALYSIS ENGINE</p>' + '<p>' + str(err) + '</p>')
            # send_email('Exception', str(err), {})
            if self.debug:
                raise err

        print('\n[END OF ANALYSIS] ->', self.asset)
        print('\nResume to follow next action', '\n------------------\n')

    def check_volume_to_buy_then_make_decision(self, type_of_trade: str):
        print('Calculating volume')
        quantity: float
        transaction_id: str
        last_price = get_last_price(self.asset, self.currency)
        quantity, transaction_id = self.calculate_volume_to_buy(type_of_trade, last_price)
        if quantity:
            success = add_trade_event(type_of_trade=type_of_trade,
                                      quantity=quantity,
                                      asset=self.asset,
                                      interval=self.interval,
                                      transaction_id=transaction_id,
                                      price=last_price,
                                      currency=self.currency)
            if success:
                print(type_of_trade.upper(), 'this', quantity, 'of', self.asset)
        else:
            print('Nothing to', type_of_trade)

    def calculate_volume_to_buy(self, type_of_trade: str, last_price: float) -> (float, str):
        if type_of_trade == 'buy':
            previous_currency_trade = get_last_trade_event_by_type_and_asset(self.asset, type_of_trade)
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
                quantity: float = define_quantity(nbr_asset_on_trade=self.length_assets, last_asset_price=last_price)
                return quantity, None

        if type_of_trade == 'sell':
            previous_currency_trade = get_last_trade_event_by_type_and_asset(self.asset, 'buy')
            # if previous_currency_trade:  # TODO -> let's try if this helps make better results
            if previous_currency_trade and last_price > previous_currency_trade['price']:
                transaction_id: str = previous_currency_trade['transactionId']
                transaction = get_transaction(transaction_id)
                return transaction['buy']['fields']['quantity'], transaction_id

        return None, None
