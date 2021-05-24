from datetime import datetime

import numpy as np
import pandas as pd
from numpy import ndarray, mean
from peakdetect import peakdetect

from src.data.marketEventUtils import get_last_minute_market_events
from src.helpers.params import MAXIMUM_PERCENTAGE_EUR
from src.services.krakenTradeService import get_account_balance


class NothingToTrade(Exception):
    super(Exception)


def define_quantity(nbr_asset_on_trade: float, last_asset_price) -> float:
    """
    Calculate the quantity of asset to buy
    :param nbr_asset_on_trade: the nbr of asset to help divide the account balance in equal sums
    :param last_asset_price: the price of the asset : money divide by asset price -> quantity to buy
    :return: the quantity to buy for a specific asset
    """
    print('\n[VOLUME TRADING QUANTITY]')
    quantity_to_buy: float
    try:
        balance_euro: float = float(get_account_balance()['result']['ZEUR'])
    except Exception as err:
        raise err

    money_available: float = (balance_euro / float(nbr_asset_on_trade)) * MAXIMUM_PERCENTAGE_EUR
    quantity_to_buy = money_available / last_asset_price
    return quantity_to_buy


# TODO -> not sure it's still useful
"""
def get_last_index(peaks_high: ndarray, peaks_low: ndarray):
    last_high_index = peaks_high[:, 0][len(peaks_high[:, 1]) - 1]
    last_low_index = peaks_low[:, 0][len(peaks_low[:, 1]) - 1]
    return last_high_index, last_low_index
"""


def generate_realtime_processed_dto_to_build_dataframe(data_object: dict) -> dict:
    """
    Get a dictionary, remove the unnecessary part then return the dictionary to add this data on a dataframe
    :param data_object: dictionary representing the processed
    :return: a dictionary which is compatible /w dataframe schema.
    """
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
    """
    Query realtime market data and remove the unnecessary raw data
    :param asset:
    :return: Null or a clean DTO to get realtime data on dataframe
    """
    last_minutes: list = get_last_minute_market_events(asset, 2)
    if last_minutes:
        last_minutes.pop()
        for res in last_minutes:
            res['timestamp'] = int(datetime.timestamp(res['time']))
        dto = generate_realtime_processed_dto_to_build_dataframe(last_minutes[len(last_minutes) - 1])
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
