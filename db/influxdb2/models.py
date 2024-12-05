import influxdb
import influxalchemy


class MyBucket(influxalchemy.Measurement):
    __measurement__ = 'mybucket'


db = influxdb.InfluxDBClient()
flux = influxalchemy.InfluxAlchemy(db)
