from datetime import datetime

# CONSTANT
DATE_STR = "%Y-%m-%dT%H:%M:%SZ"
DATE_UTC_TZ_STR = "%Y-%m-%d %H:%M:%S.%f+00:00"
SIMPLE_DATE_STR = "%Y-%m-%d %H:%M"


# METHOD
def set_datetime(datetime_str):
    return datetime.strptime(datetime_str, DATE_STR)
