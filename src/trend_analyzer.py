from src.email_sender_helper import send_email
from src.timeseries_service import addEvent
from src.trend_analyzer_helper import get_last_index, calculate_volume_to_buy, find_multiple_curve_min_max


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
                volume_to_buy = calculate_volume_to_buy(self, typeOfTrade, attachments)
                if volume_to_buy:
                    addEvent(typeOfTrade, volume_to_buy,
                             self.df, self.index_size - 1)
                    send_email(
                        '[BOT-ANALYSIS]', 'Incoming trade : [' + self.asset + '] ' + typeOfTrade,
                        attachments)
                    print(typeOfTrade, 'this', volume_to_buy)
                else:
                    print('Nothing to', typeOfTrade)

            elif self.last_close_high <= self.index_size - 5 or self.last_macd_high <= self.index_size - 5:
                typeOfTrade = 'sell'
                volume_to_buy = calculate_volume_to_buy(self, typeOfTrade, attachments)
                if volume_to_buy:
                    addEvent(typeOfTrade, volume_to_buy,
                             self.df, self.index_size - 1)
                    send_email(
                        '[BOT-ANALYSIS]', 'Incoming trade : [' + self.asset + '] ' + typeOfTrade,
                        attachments)
                    print(typeOfTrade, 'this', volume_to_buy)
                else:
                    print('Nothing to', typeOfTrade)

        except Exception as err:
            send_email('Exception', str(err), {})

        print('[END OF ANALYSIS] ->', self.asset)
        print('\nResume to next asset')
