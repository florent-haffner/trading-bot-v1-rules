from requests import get

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

__KRAKEN_API = "https://api.kraken.com/0/public/OHLC"


class RequestToKrakenError(Exception): pass


"""
:param asset -> the pair of currency, ex : BTCEUR, ETHEUR, ALGOUSD
:param interval -> data interval in minutes (1, 5, 10, 60, 120, 360, 1440)
"""
def getDatasFromKraken(asset, interval) -> object:
    URL = __KRAKEN_API + '?pair=' + asset + '&interval=' + interval
    try:
        res = get(URL)
        if len(res.json()['error']) > 0:
            raise RequestToKrakenError('Unable to reach proper datas')
        return res.json()

    except Exception as err:
        raise err


"""
:param apiResponse -> datas from api
:return pandas Dataframe object
"""
def getDataframe(apiResponse) -> pd.DataFrame:
    firstMapKey = list(apiResponse['result'].keys())[0]
    schema = ['timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
    df = pd.DataFrame(apiResponse['result'][firstMapKey], columns=schema)
    df.sort_values(by=['timestamp'])

    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['vwap'] = df['vwap'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df['count'] = df['count'].astype(float)
    return df


"""
Glue everything together
"""
def getFormattedData(asset, interval) -> pd.DataFrame:
    print('Quering ' + asset + '\'s on interval ' + interval + 'min from Kraken')
    datas = getDatasFromKraken(asset, interval)
    return getDataframe(datas)


"""
Help split dataset
:param full_dataset -> straight forward
:param split_radio -> value between 0 & 1, like 0.85 for example
:return properly splitted train_dataset and test_dataset
"""
def splitDataset(full_dataset, split_ratio) -> [pd.DataFrame]:
    split_length = int(len(full_dataset) * split_ratio)
    train_set = full_dataset[:split_length]
    test_set = full_dataset[split_length:]
    return train_set, test_set


def getXy(dataset, X_key, y_key) -> [pd.DataFrame]:
    try:
        return dataset[X_key], dataset[y_key]
    except KeyError:
        raise KeyError('Error with the keys', X_key, ' or ', y_key)


"""
:param get X, y
:return scaled dataset from 0 to 1
"""
def process_data_to_scale(scaler, X, y) -> [MinMaxScaler]:
    X_scaled = scaler.fit_transform(
        X.values.reshape(len(X.values),
                         1)
    )
    y_scaled = scaler.fit_transform(
        y.values.reshape(len(y.values),
                         1)
    )
    return X_scaled, y_scaled


if __name__ == "__main__":
    df = getFormattedData('BTCEUR', '60')
    df.plot('timestamp', 'volume')
    # plt.show()

    train, test = splitDataset(df, .85)
    X, y = getXy(train, 'volume', 'timestamp')

    # Pre-process data to scale to 0->1
    scaler = MinMaxScaler()
    X_train, y_train = process_data_to_scale(scaler, X, y)
    print(X_train, y_train)

    inverse = scaler.inverse_transform(y_train)
    print(inverse)
