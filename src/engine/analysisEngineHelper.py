from typing import Dict, Any
import pandas as pd

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
