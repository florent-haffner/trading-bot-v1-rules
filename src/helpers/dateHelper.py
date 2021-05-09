from datetime import datetime

# CONSTANT
DATE_STR: str = "%Y-%m-%dT%H:%M:%SZ"
DATE_UTC_TZ_STR: str = "%Y-%m-%d %H:%M:%S.%f+00:00"
SIMPLE_DATE_STR: str = "%Y-%m-%d %H:%M"


# METHOD
def set_datetime(datetime_str) -> datetime:
    return datetime.strptime(datetime_str, DATE_STR)
