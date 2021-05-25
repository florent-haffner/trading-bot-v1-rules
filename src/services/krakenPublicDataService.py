from typing import Dict

import pandas as pd
from requests import get, Response

from stockstats import StockDataFrame

__KRAKEN_API = "https://api.kraken.com/0/public/OHLC"


class RequestToKrakenError(Exception):
    super(Exception)


def get_data_from_kraken(asset: str, interval: str) -> Dict:
    """
    :param asset : the pair of currency -> BTCEUR, ETHEUR, ALGOUSD
    :param interval : mock interval in minutes (1, 5, 10, 60, 120, 360, 1440)
    """
    URL: str = __KRAKEN_API + '?pair=' + asset + '&interval=' + interval
    try:
        res: Response = get(URL)
        if len(res.json()['error']) > 0:
            raise RequestToKrakenError('Unable to reach proper datas')
        return res.json()
    except Exception as err:
        raise err


def get_dataframe(api_response: dict) -> pd.DataFrame:
    """
    :param api_response -> datas from api
    :return pandas Dataframe object
    """
    firstMapKey = list(api_response['result'].keys())[0]
    schema = ['timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
    dataframe: pd.DataFrame = pd.DataFrame(api_response['result'][firstMapKey], columns=schema)
    dataframe.sort_values(by=['timestamp'])

    dataframe['open'] = dataframe['open'].astype(float)
    dataframe['high'] = dataframe['high'].astype(float)
    dataframe['low'] = dataframe['low'].astype(float)
    dataframe['close'] = dataframe['close'].astype(float)
    dataframe['vwap'] = dataframe['vwap'].astype(float)
    dataframe['volume'] = dataframe['volume'].astype(float)
    dataframe['count'] = dataframe['count'].astype(float)
    return dataframe


def get_formatted_data(asset, interval) -> pd.DataFrame:
    """
    Glue everything together
    :param asset:
    :param interval:
    :return:
    """
    print('\n--------------------------------------------------\n',
          '[QUERY] - Kraken - ', asset + ' on ' + interval + 'min')
    results: Dict = get_data_from_kraken(asset, interval)
    return get_dataframe(results)


# """
# :param get X, y
# :return scaled dataset from 0 to 1
# """
# def process_data_to_scale(scaler, X, y) -> [MinMaxScaler]:
#     X_scaled = scaler.fit_transform(
#         X.values.reshape(len(X.values),
#                          1)
#     )
#     y_scaled = scaler.fit_transform(
#         y.values.reshape(len(y.values),
#                          1)
#     )
#     return X_scaled, y_scaled


def get_stocks_indicators(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe: pd.DataFrame = StockDataFrame.retype(dataframe)
    dataframe['macd'] = dataframe.get('macd')
    dataframe['ema'] = dataframe.get('dx_6_ema')
    dataframe['close_12_ema'] = dataframe.get('close_12_ema')
    dataframe['close_26_ema'] = dataframe.get('close_26_ema')
    return dataframe


if __name__ == "__main__":
    df = get_formatted_data('BTCEUR', '60')
    df.plot('timestamp', 'volume')
    # plt.show()

    """
    train, test = splitDataset(df, .85)
    X, y = getXy(train, 'volume', 'timestamp')

    # Pre-process mock to scale to 0->1
    scaler = MinMaxScaler()
    X_train, y_train = process_data_to_scale(scaler, X, y)
    print(X_train, y_train)

    inverse = scaler.inverse_transform(y_train)
    print(inverse)
    """
