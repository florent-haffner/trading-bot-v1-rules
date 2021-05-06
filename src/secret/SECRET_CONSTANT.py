import urllib.parse

__EMAIL_USER = "moneymakr.bot@gmail.com"
__EMAIL_PASSWORD = "z5bDm#!gs^8$2Z"

__MONGO_PROTOCOL = "mongodb+srv"
__MONGO_HOST = "cluster0.njz0p.mongodb.net/tradingbot?retryWrites=true&w=majority"
__MONGO_USER = "mongobot"
__MONGO_PASSWORD = "QUu1fh00YkMQ3AcR"

__MONGO_URI = __MONGO_PROTOCOL + "://" +\
              __MONGO_USER + ":" + urllib.parse.quote_plus(__MONGO_PASSWORD) +\
              "@" + __MONGO_HOST

# __INFLUX_URI = ""
# __INFLUX_TOKEN = ""
__INFLUX_URI = "https://eu-central-1-1.aws.cloud2.influxdata.com"
__INFLUX_TOKEN = "a3F2tgV39YMq55Sd_V7VFZbdtqwJTPMSs_jmjmkd-ttsGr61z6jWk1q2_grZ89PZBMHGlXXlP350QYIUgGYHFw=="

__INFLUX_HOST = "192.168.1.58"
__INFLUX_PORT = 8086
__INFLUX_USER = "influxroot"
__INFLUX_PASSWORD = "4s&6Q@6zxNE2Yn"
__INFLUX_DB_TRADE_EVENT = "ts_trade_event"
