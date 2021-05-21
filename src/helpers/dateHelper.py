from datetime import datetime
import pytz

# CONSTANT
DATE_STR: str = "%Y-%m-%dT%H:%M:%SZ"
DATE_UTC_TZ_STR: str = "%Y-%m-%d %H:%M:%S.%f+00:00"
SIMPLE_DATE_STR: str = "%Y-%m-%d %H:%M"


def set_datetime(datetime_str: str) -> datetime:
    """ Get a string input and return a datetime object """
    return datetime.strptime(datetime_str, DATE_STR)


def set_timezone(time: datetime) -> datetime:
    """ Get a datetime input, add timezone then return a proper datetime object """
    europe_paris = pytz.timezone('Europe/Paris')
    return time.astimezone(europe_paris)
