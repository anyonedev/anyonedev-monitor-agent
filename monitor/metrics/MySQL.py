'''
Created on 2014-11-15

@author: hongye
'''
import mysql.connector
from core.MetricValue import BatchMultiMetricValue, MultiMetricValue

from config import config

def mysql_slowlog_parser(line):
    pass


from core.MonitorSource import SampleMonitorSource

class MySQLMonitorSource(SampleMonitorSource):
    _conn = None
    _mysqlConfig = None
    def start(self):
        if self._mysqlConfig == None:
            self._conn = mysql.connector.Connect(**config.mysqlConfig)
        else:
            self._conn = mysql.connector.Connect(**self._mysqlConfig)
            
    def stop(self):
        if self._conn != None:
            self._conn.close()
    
    def mysqlConfig(self, config):
        self._mysqlConfig = config
        return self

class ShowGlobalStatusMonitorSource(MySQLMonitorSource):
    _query = "select VARIABLE_NAME,VARIABLE_VALUE from _global_status_wrapper"
    
    def sample(self,parms):
        cursor = self._conn.cursor()
        cursor.execute(self._query)
        rows = cursor.fetchall()
        values = dict()
        for row in rows:
            values[row[0]] = row[1]
        
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.setValues(values)
        
        return metricValue

def mysql_show_global_status(monitorSourceName):
    return ShowGlobalStatusMonitorSource().monitorSourceName(monitorSourceName)

class DataSizePerSchemaMonitorSource(MySQLMonitorSource):
    _query = "select * from data_size_per_schema"
    def sample(self, parms):
        cursor = self._conn.cursor()
        cursor.execute(self._query)
        rows = cursor.fetchall()
        values = []
        for x in rows:
            values.append(dict(zip(cursor.column_names, x)))
        metricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        metricValue.setValues(values)
        return metricValue

def mysql_data_size_per_schema(monitorSourceName):
    return DataSizePerSchemaMonitorSource().monitorSourceName(monitorSourceName)

if __name__ == '__main__':
    monitorSource = ShowGlobalStatusMonitorSource()
    monitorSource.start()
    metricValue = monitorSource.sample(None)
    print(metricValue.getValues())
