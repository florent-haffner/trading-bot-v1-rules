from datetime import datetime
from typing import Dict, Any
import pandas as pd

from src.data.marketEventUtils import getLastMinuteMarketEvents
from src.helpers.dateHelper import set_timezone
from src.helpers.params import MAXIMUM_PERCENTAGE_EUR
from src.services.krakenTradeService import getAccountBalance


class NothingToTrade(Exception):
    super(Exception)


def define_volume(df: pd.DataFrame, type_of_trade: str, nbr_asset_on_trade: float, index_max: int) -> float:
    print('\n[VOLUME TRADING QUANTITY]')
    print('Type of trade:', type_of_trade)
    volume_to_buy: float
    try:
        balance_euro: float = float(getAccountBalance()['result']['ZEUR'])
        money_available: float = (balance_euro / float(nbr_asset_on_trade)) * MAXIMUM_PERCENTAGE_EUR
        volume_to_buy: float = money_available / df['close'][index_max]
    except Exception as err:
        raise err
    return volume_to_buy


def build_dto(df, measures, index) -> Dict:
    DTO: Dict[str, Any] = {}
    for measure in measures:
        DTO[measure] = df[measure][index]
    return DTO


def get_last_index(peaks_high, peaks_low):
    last_high_index = peaks_high[:, 0][len(peaks_high[:, 1]) - 1]
    last_low_index = peaks_low[:, 0][len(peaks_low[:, 1]) - 1]
    return last_high_index, last_low_index


def generate_realtime_processed_dto(data_object):
    keys_to_keep = ['timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
    # Generate needed keys
    for item in range(len(keys_to_keep)):
        try:
            print(keys_to_keep[item], data_object[keys_to_keep[item]])
        except KeyError:
            data_object[keys_to_keep[item]] = 0.
    # Remove unneeded keys
    for key in list(data_object.keys()):
        if key not in keys_to_keep:
            del data_object[key]
    return data_object


def get_realtime_processed_asset(asset):
    last_minutes = getLastMinuteMarketEvents(asset, 2)
    last_minutes.pop()

    for res in last_minutes:
        res['timestamp'] = int(datetime.timestamp(res['time']))

    return generate_realtime_processed_dto(last_minutes[len(last_minutes) - 1])


if __name__ == '__main__':
    get_realtime_processed_asset('ALGO')
