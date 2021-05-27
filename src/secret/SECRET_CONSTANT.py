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
# __MONGO_PROTOCOL: String = ""
# __MONGO_HOST: String = ""
# __MONGO_USER: String = ""
# __MONGO_PASSWORD: String = ""
# __MONGO_DB: String = ""

__MONGO_PROTOCOL: String = "mongodb+srv"
__MONGO_HOST: String = "cluster0.njz0p.mongodb.net/tradingbot?retryWrites=true&w=majority"
__MONGO_USER: String = "mongobot"
__MONGO_PASSWORD: String = "QUu1fh00YkMQ3AcR"
__MONGO_DB: String = "trading_bot"

__MONGO_URI: String = __MONGO_PROTOCOL + "://" +\
              __MONGO_USER + ":" + urllib.parse.quote_plus(__MONGO_PASSWORD) +\
              "@" + __MONGO_HOST


"""
    DATABASES - InfluxDB
"""
# __INFLUX_URI = ""
# __INFLUX_TOKEN = ""
__INFLUX_URI: String = "https://eu-central-1-1.aws.cloud2.influxdata.com"
__INFLUX_TOKEN: String = "a3F2tgV39YMq55Sd_V7VFZbdtqwJTPMSs_jmjmkd-ttsGr61z6jWk1q2_grZ89PZBMHGlXXlP350QYIUgGYHFw=="

# __INFLUX_BUCKET_TRADE_EVENT: String = ""
# __INFLUX_BUCKET_MARKET_EVENT: String = ""
__INFLUX_BUCKET_TRADE_EVENT: String = "ts_trade_event"
__INFLUX_BUCKET_MARKET_EVENT: String = "ts_market_event"
