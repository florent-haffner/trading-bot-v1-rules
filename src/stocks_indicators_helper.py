from stockstats import StockDataFrame


def get_stocks_indicators(df):
    df = StockDataFrame.retype(df)
    df['macd'] = df.get('macd')
    df['ema'] = df.get('dx_6_ema')
    df['close_12_ema'] = df.get('close_12_ema')
    df['close_26_ema'] = df.get('close_26_ema')
    return df
