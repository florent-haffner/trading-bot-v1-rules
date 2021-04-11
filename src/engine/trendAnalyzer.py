from src.helpers.emailSenderHelper import send_email
from src.services.timeseriesService import addEvent
from src.engine.trendAnalyzerHelper import get_last_index, calculate_volume_to_buy, find_multiple_curve_min_max


class TrendAnalyzer:
    def __init__(self, df, asset, currency, length_assets, interval):
        self.df = df
        self.asset = asset
        self.currency = currency
        self.length_assets = length_assets
        self.interval = interval

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
        print('close index { high:', self.last_close_high, ' low:', self.last_close_low, '}')

    def make_decision(self):
        print('\n[DECISION MAKING]')
        attachments = [self.pathFigCLOSE, self.pathFigMACD]
        try:
            margin = 10
            if self.last_close_low >= self.index_size - margin or \
                    self.last_macd_low >= self.index_size - margin:
                typeOfTrade = 'buy'
                self.create_trade_event(typeOfTrade, attachments)

            elif self.last_close_high >= self.index_size - margin or \
                    self.last_macd_high >= self.index_size - margin:
                typeOfTrade = 'sell'
                self.create_trade_event(typeOfTrade, attachments)
            else:
                print('Trends are currently evolving, waiting...')

        except Exception as err:
            print('[EXCEPTION] - sending email', err)
            send_email('Exception', str(err), {})

        print('[END OF ANALYSIS] ->', self.asset)
        print('\nResume to next asset')

    def create_trade_event(self, type_of_trade, attachments):
        volume_to_buy = calculate_volume_to_buy(self, type_of_trade, attachments)
        if volume_to_buy:
            addEvent(type_of_trade=type_of_trade,
                     volume_to_buy=volume_to_buy,
                     asset=self.asset,
                     df=self.df,
                     maximum_index=self.index_size - 1,
                     interval=self.interval)
            send_email(
                '[BOT-ANALYSIS]', 'Incoming trade : [' + self.asset + '] - type: ' + type_of_trade,
                attachments)
            print(type_of_trade, 'this', volume_to_buy, 'of', self.asset)
        else:
            print('Nothing to', type_of_trade)
