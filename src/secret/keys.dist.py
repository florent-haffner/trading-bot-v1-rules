import urllib.parse
from tokenize import String


"""
    CONTACT - EMAIL
"""
__EMAIL_USER: String = ""
__EMAIL_PASSWORD: String = ""


"""
    DATABASES - MongoDB
"""
__MONGO_PROTOCOL: String = ""
__MONGO_HOST: String = ""
__MONGO_USER: String = ""
__MONGO_PASSWORD: String = ""
__MONGO_DB: String = ""

__MONGO_URI: String = __MONGO_PROTOCOL + "://" +\
              __MONGO_USER + ":" + urllib.parse.quote_plus(__MONGO_PASSWORD) +\
              "@" + __MONGO_HOST


"""
    DATABASES - InfluxDB
"""
__INFLUX_URI: String = ""
__INFLUX_TOKEN: String = ""

__INFLUX_BUCKET_TRADE_EVENT: String = "ts_trade_event"
__INFLUX_BUCKET_MARKET_EVENT: String = "ts_market_event"
