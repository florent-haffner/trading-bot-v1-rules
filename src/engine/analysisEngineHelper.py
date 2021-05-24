from datetime import datetime
from typing import Dict, Any

import numpy as np
import pandas as pd
from numpy import ndarray, mean
from peakdetect import peakdetect

from src.data.marketEventUtils import get_last_minute_market_events
from src.helpers.params import MAXIMUM_PERCENTAGE_EUR
from src.services.krakenTradeService import get_account_balance


class NothingToTrade(Exception):
    super(Exception)


def define_quantity(type_of_trade: str, nbr_asset_on_trade: float, price) -> float:
    print('\n[VOLUME TRADING QUANTITY]')
    print('Type of trade:', type_of_trade)
    quantity_to_buy: float
    try:
        balance_euro: float = float(get_account_balance()['result']['ZEUR'])
    except Exception as err:
        raise err

    money_available: float = (balance_euro / float(nbr_asset_on_trade)) * MAXIMUM_PERCENTAGE_EUR
    quantity_to_buy = money_available / price
    return quantity_to_buy


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
    print(data_object)
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


def query_realtime_processed_by_asset(asset: str) -> object:
    last_minutes: list = get_last_minute_market_events(asset, 2)
    if last_minutes:
        last_minutes.pop()
        for res in last_minutes:
            res['timestamp'] = int(datetime.timestamp(res['time']))
        dto = generate_realtime_processed_dto(last_minutes[len(last_minutes) - 1])
        if dto['close'] and dto['volume']:
            return dto
    return None


def compute_mean_peaks(df: pd.DataFrame, margin: int):
    """
    Handle the peak calculation to compute statistics over trend
    :param df: input data
    :param margin: the number of point it needs to calculate a peak
    :return:
    """
    peaks = peakdetect(df['close'], lookahead=margin)
    higher_peaks: ndarray = np.array(peaks[0])
    lower_peaks: ndarray = np.array(peaks[1])

    last_event: float = df['close'][len(df) - 1]
    high_mean: float = float(mean(higher_peaks[:, 1]))
    low_mean: float = float(mean(lower_peaks[:, 1]))
    return high_mean, low_mean, higher_peaks, lower_peaks, last_event
