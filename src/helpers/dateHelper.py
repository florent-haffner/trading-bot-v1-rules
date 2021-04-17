from datetime import datetime

from src.helpers.CONSTANT import DATE_STR


def set_datetime(datetime_str):
    return datetime.strptime(datetime_str, DATE_STR)
