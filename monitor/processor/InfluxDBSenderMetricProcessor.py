'''
Created on 2014-11-12

@author: hongye
'''

from influxdb.client import InfluxDBClient

from config import config
from core import MetricValue
from core.MetricProcessor import MetricProcessor
from core.MetricValue import MultiMetricValue, SingleMetricValue, \
    BatchMultiMetricValue, KeyedMultiMetricValue


class InfluxDBSenderMetricProcessor(MetricProcessor):
    _host = config.influxDBSender.get("host")
    _username = config.influxDBSender.get("username")
    _password = config.influxDBSender.get("password")
    _database = config.influxDBSender.get("database")
    _port = config.influxDBSender.get("port")
    client = None
    
    def start(self):
        self.client = InfluxDBClient(self._host, self._port, self._username, self._password, self._database)
        
    def process(self, metricValue:MetricValue):
        clientId = metricValue.getClientId()
        monitorSourceName = metricValue.getMonitorSourceName()
        sampleTime = metricValue.getSampleTime()
        data = []
        
        if isinstance(metricValue, MultiMetricValue):
            value = {"name":clientId + "." + monitorSourceName}
            columns = ["time"]
            point = [sampleTime]
            for (k, v) in metricValue.getValues().items():
                columns.append(k)
                point.append(v)
            value["columns"] = columns
            value["points"] = [point]
            data.append(value)
        elif isinstance(metricValue, SingleMetricValue):
            value = {"name":clientId + "." + monitorSourceName}
            columns = ["time", "value"]
            point = [sampleTime, metricValue.getMetricValue()]
            value["columns"] = columns
            value["points"] = [point]
            data.append(value)
        elif isinstance(metricValue, BatchMultiMetricValue):
            for mv in metricValue.getValues():
                value = {"name":clientId + "." + monitorSourceName}
                columns = ["time"]
                point = [sampleTime]
                for (k, v) in mv.items():
                    columns.append(k)
                    point.append(v)
                value["columns"] = columns
                value["points"] = [point]
                data.append(value)                
        elif isinstance(metricValue, KeyedMultiMetricValue):
            for (key, mv) in metricValue.getValues().items():
                value = {"name":clientId + "." + monitorSourceName + "." + key}
                columns = ["time"]
                point = [sampleTime]
                for (k, v) in mv.items():
                    columns.append(k)
                    point.append(v)
                value["columns"] = columns
                value["points"] = [point]
                data.append(value)
        else:
            pass

        self.client.write_points_with_precision(data, 'ms')
        
    def host(self, host):
        self._host = host
        return self
    
    def username(self, username):
        self._username = username
        return self
    
    def password(self, password):
        self._password = password
        return self
        
    def database(self, database):
        self._database = database
        return self
    
    def port(self, port):
        self._port = port
        return self
    
