from CONSTANT import __INFLUX_HOST, __INFLUX_PORT, __INFLUX_USER, __INFLUX_PASSWORD, __INFLUX_DB_PRICE, __INFLUX_DB_ACTIONS
from influxdb import InfluxDBClient

__INFLUX_CLIENT = InfluxDBClient(
    host=__INFLUX_HOST,
    port=__INFLUX_PORT,
    username=__INFLUX_USER,
    password=__INFLUX_PASSWORD
)


def getAllStockActions():
    print('none')


JSON = [
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2021-04-01T8:01:00Z",
        "fields": {
            "duration": 127
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2021-04-01T8:04:00Z",
        "fields": {
            "duration": 132
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2021-04-01T8:02:00Z",
        "fields": {
            "duration": 129
        }
    }
]


if __name__ == "__main__":
    print('Config InfluxDB')
    __INFLUX_CLIENT.create_database(__INFLUX_DB_PRICE)
    __INFLUX_CLIENT.create_database(__INFLUX_DB_ACTIONS)
    print('DBs', __INFLUX_CLIENT.get_list_database())

    tmp_DB = 'timeseries'
    __INFLUX_CLIENT.switch_database(tmp_DB)
    __INFLUX_CLIENT.write_points(JSON)

    query = 'SELECT "duration" FROM '+tmp_DB+'."autogen"."brushEvents" WHERE time > now() - 30d GROUP BY "user"'
    res = __INFLUX_CLIENT.query(query)
    print(res)
