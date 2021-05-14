import urllib.parse
from tokenize import String


"""
    CONTACT - EMAIL
"""
__EMAIL_USER: String = "moneymakr.bot@gmail.com"
__EMAIL_PASSWORD: String = "z5bDm#!gs^8$2Z"

"""
    CONTACT - TELEGRAM
"""
__TELEGRAM_PHONE_NBR: String = "33698671845"
__TELEGRAM_APP_ID: String = "4532406"
__TELEGRAM_APP_HASH: String = "992dea81cfb81f6192653eb8c9011f8e"
__TELEGRAM_APP_TOKEN: String = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvmpxVY7ld/8DAjz6F6q0
5shjg8/4p6047bn6/m8yPy1RBsvIyvuDuGnP/RzPEhzXQ9UJ5Ynmh2XJZgHoE9xb
nfxL5BXHplJhMtADXKM9bWB11PU1Eioc3+AXBB8QiNFBn2XI5UkO5hPhbb9mJpjA
9Uhw8EdfqJP8QetVsI/xrCEbwEXe0xvifRLJbY08/Gp66KpQvy7g8w7VB8wlgePe
xW3pT13Ap6vuC+mQuJPyiHvSxjEKHgqePji9NP3tJUFQjcECqcm0yV7/2d0t/pbC
m+ZH1sadZspQCEPPrtbkQBlvHb4OLiIWPGHKSMeRFvp3IWcmdJqXahxLCUS1Eh6M
AQIDAQAB
-----END PUBLIC KEY-----
"""

"""
    DATABASES - MongoDB
"""
__MONGO_PROTOCOL: String = "mongodb+srv"
__MONGO_HOST: String = "cluster0.njz0p.mongodb.net/tradingbot?retryWrites=true&w=majority"
__MONGO_USER: String = "mongobot"
__MONGO_PASSWORD: String = "QUu1fh00YkMQ3AcR"

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

__INFLUX_HOST: String = "192.168.1.58"
__INFLUX_PORT: int = 8086
__INFLUX_USER: String = "influxroot"
__INFLUX_PASSWORD: String = "4s&6Q@6zxNE2Yn"
__INFLUX_DB_TRADE_EVENT: String = "ts_trade_event"
