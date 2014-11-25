'''
Created on 2014-11-12

@author: hongye
'''

from core.MetricProcessor import MetricProcessor
from core.MetricValue import MetricValue, MultiMetricValue, SingleMetricValue
from utils.Logger import info


class LoggingMetricProcessor(MetricProcessor):
    
    def start(self):
        pass
    
    def process(self, metricValue:MetricValue):
        clientId = metricValue.getClientId()
        monitorSourceName = metricValue.getMonitorSourceName()
        sampleTime = metricValue.getSampleTime() 
        
        if isinstance(metricValue, MultiMetricValue):
            info(metricValue.getValues())
        elif isinstance(metricValue, SingleMetricValue):
            info(metricValue.getMetricValue())
        
        
    def stop(self):
        pass
    
    def fail(self):
        pass     
