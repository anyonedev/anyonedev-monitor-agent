'''
Created on 2014-11-12

@author: hongye
'''

from builtins import round, int
from time import time

from config import config


OK = 1
KO = 0

class MetricValue(object):
    _clientId = None
    _monitorSourceName = ""
    _sampleTime = 0
    _status = OK
    
    def __init__(self):
        self._sampleTime = int(round(time() * 1000))
        self._clientId = config.clientId
        
    
    def getMonitorSourceName(self):
        return self._monitorSourceName
    
    def getSampleTime(self):
        return self._sampleTime
    
    def sampleTime(self):
        self._sampleTime = int(round(time() * 1000))
    
    def getClientId(self):
        return self._clientId
    
    def monitorSourceName(self, name):
        self._monitorSourceName = name
        return self
    def getStatus(self):
        return self._status
    
    def status(self, status):
        self._status = status
        return self

class SingleMetricValue(MetricValue):
    name = None
    value = None
    
    def __init__(self, monitorSourceName="", name=None, value=None):
        MetricValue.__init__(self)
        self.monitorSourceName(monitorSourceName)
        self.name = name
        self.value = value
    
    def getMetricName(self):
        return self.name
    
    def getMetricValue(self):
        return self.value
    
    def metricName(self, name):
        self.name = name
        return self
    
    def metricValue(self, value):
        self.value = value
        return self

class MultiMetricValue(MetricValue):
    _values = dict()
    def __init__(self, monitorSourceName=""):
        MetricValue.__init__(self)
        self._values = dict()
        self.monitorSourceName(monitorSourceName)
    
    def addMetricValue(self, name, value):
        self._values[name] = value
    
    def addMetricValues(self, values):
        if values == None:
            return 
        for (k, v) in values.items():
            self._values[k] = v
    
    def getValue(self, name):
        return self._values.get(name)
                  
    def getValues(self):
        return self._values
    
    def setValues(self,values):
        self._values = values

class BatchMultiMetricValue(MetricValue):
    _values = []
    def __init__(self, monitorSourceName=""):
        MetricValue.__init__(self)
        self._values = []
        self.monitorSourceName(monitorSourceName)
        
    def addMetricValue(self, values):
        self._values.append(values)
        
    def getValues(self):
        return self._values
    
    def setValues(self,values):
        self._values = values

class KeyedMultiMetricValue(MetricValue):
    _values = dict()
    
    def __init__(self, monitorSourceName=""):
        MetricValue.__init__(self)
        self._values = dict()
        self.monitorSourceName(monitorSourceName)
        
    def addMetricValue(self, name, metricValue):
#         if self._values.get(name) != None:
#             raise Exception()
        self._values[name] = metricValue
    
    def getValues(self):
        return self._values
    
