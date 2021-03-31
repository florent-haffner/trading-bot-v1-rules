from stockstats import StockDataFrame


def get_stocks_indicators(df):
    df = StockDataFrame.retype(df)
    df['macd'] = df.get('macd')  # calculate MACD
    df['close_12_ema'] = df.get('close_12_ema')  # calculate MACD
    df['close_26_ema'] = df.get('close_26_ema')  # calculate MACD
    return df
