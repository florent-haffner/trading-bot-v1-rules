import urllib.parse
from tokenize import String

__EMAIL_USER: String = "moneymakr.bot@gmail.com"
__EMAIL_PASSWORD: String = "z5bDm#!gs^8$2Z"

__MONGO_PROTOCOL: String = "mongodb+srv"
__MONGO_HOST: String = "cluster0.njz0p.mongodb.net/tradingbot?retryWrites=true&w=majority"
__MONGO_USER: String = "mongobot"
__MONGO_PASSWORD: String = "QUu1fh00YkMQ3AcR"

__MONGO_URI: String = __MONGO_PROTOCOL + "://" +\
              __MONGO_USER + ":" + urllib.parse.quote_plus(__MONGO_PASSWORD) +\
              "@" + __MONGO_HOST

# __INFLUX_URI = ""
# __INFLUX_TOKEN = ""
__INFLUX_URI: String = "https://eu-central-1-1.aws.cloud2.influxdata.com"
__INFLUX_TOKEN: String = "a3F2tgV39YMq55Sd_V7VFZbdtqwJTPMSs_jmjmkd-ttsGr61z6jWk1q2_grZ89PZBMHGlXXlP350QYIUgGYHFw=="

__INFLUX_HOST: String = "192.168.1.58"
__INFLUX_PORT: int = 8086
__INFLUX_USER: String = "influxroot"
__INFLUX_PASSWORD: String = "4s&6Q@6zxNE2Yn"
__INFLUX_DB_TRADE_EVENT: String = "ts_trade_event"
