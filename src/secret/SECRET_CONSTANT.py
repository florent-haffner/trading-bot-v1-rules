import urllib.parse

__EMAIL_USER = "moneymakr.bot@gmail.com"
__EMAIL_PASSWORD = "z5bDm#!gs^8$2Z"

__MONGO_PROTOCOL = "mongodb"
__MONGO_HOST = "192.168.1.58:27017"
__MONGO_USER = "mongoroot"
__MONGO_PASSWORD = "f$8A#@f3uYgU^o"

__MONGO_URI = __MONGO_PROTOCOL + "://" +\
              __MONGO_USER + ":" + urllib.parse.quote_plus(__MONGO_PASSWORD) +\
              "@" + __MONGO_HOST

__INFLUX_URI = ""
__INFLUX_TOKEN = ""

__INFLUX_HOST = "192.168.1.58"
__INFLUX_PORT = 8086
__INFLUX_USER = "influxroot"
__INFLUX_PASSWORD = "4s&6Q@6zxNE2Yn"
__INFLUX_DB_TRADE_EVENT = "ts_trade_event"
