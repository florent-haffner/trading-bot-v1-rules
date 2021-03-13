from requests import get
import pandas as pd
import matplotlib.pyplot as plt

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


def getFormattedData(asset, interval) -> pd.DataFrame:
    print('Quering ' + asset + '\'s on interval ' + interval + 'min from Kraken')
    datas = getDatasFromKraken(asset, interval)
    return getDataframe(datas)


def splitDataset(full_dataset, split_ratio):
    split_length = int(len(full_dataset) * split_ratio)
    train_set = full_dataset[:split_length]
    test_set = full_dataset[split_length:]
    return train_set, test_set

if __name__ == "__main__":
    # df = getFormattedData('BTCEUR', '1')
    # df.plot('timestamp', 'volume')
    # plt.show()

    train, test = splitDataset([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], .85)
    print(train, test)
