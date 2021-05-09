from typing import Dict, Any
import pandas as pd

from src.helpers.params import MAXIMUM_PERCENTAGE_EUR
from src.services.krakenTradeService import getAccountBalance


class NothingToTrade(Exception): pass


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


# TODO -> remove these unused part of codebase
"""
def plot_peaks_close_ema(df, key, higher_peaks, lower_peaks):
    fig = plt.figure()
    plt.ion()
    plt.title(key)
    plt.plot(df[key])
    plt.plot(df['close_12_ema'])
    # if key == 'close_12_ema':
    #     plt.plot(df['close'])

    plt.plot(higher_peaks[:, 0], higher_peaks[:, 1], 'ro')
    plt.plot(lower_peaks[:, 0], lower_peaks[:, 1], 'go')

    path_to_save_figure = '/tmp/' + str(datetime.now()) + '-' + key + '.png'
    plt.savefig(path_to_save_figure)
    plt.close('all')
    return path_to_save_figure


def find_multiple_curve_min_max(df, key, nbr_occurrences):
    print('CURVE - ', key, '- Detecting peaks min/max')
    length_df = len(df)
    if df[key][length_df - 1] > 0:
        print('POSITIVE')
    else:
        print('NEGATIVE')

    peaks = peakdetect(df[key], lookahead=nbr_occurrences)
    higher_peaks = np.array(peaks[0])
    lower_peaks = np.array(peaks[1])

    path_fig = plot_peaks_close_ema(df, key, higher_peaks, lower_peaks)
    return higher_peaks, lower_peaks, path_fig

def remove_tmp_pics(path):
    try:
        os.remove(path)
        print('Removed tmp plot figure from', path)
    except OSError:
        pass
"""
