'''
Created on 2014-11-12

@author: hongye
'''

from _testcapi import traceback_print
from builtins import Exception
import traceback

from core import monitorSourceRegistry
from core import schedudler
from core.MetricProcessor import MetricProcessor
from core.MetricValue import MetricValue
from core.MonitorSource import SampleMonitorSource


class ScheduleMetricProcessor(MetricProcessor):
    
    monitorSourceMatcher = None
    metricProcessor = None
    
    triggerType = "interval" 
    interval = 1
    
    def start(self):
        schedudler.add_interval_job(self.job_function, seconds=self.interval)
        self.metricProcessor.start()
    
    def job_function(self):
        try:
            monitorSources = monitorSourceRegistry.getByMonitorSourceMatcher(self.monitorSourceMatcher)
            for monitorSource in monitorSources:
                if isinstance(monitorSource, SampleMonitorSource):
                    metricValue = monitorSource.sample(None)
                    self.process(metricValue)
        except Exception:
            print(traceback.format_exc())
            
    def process(self, metricValue:MetricValue):
        self.metricProcessor.process(metricValue)
    
    def stop(self):
        pass
    
    def fail(self):
        pass
    
    def interval(self, interval, monitorSourceMatcher, processor):
        self.interval = interval
        self.monitorSourceMatcher = monitorSourceMatcher
        self.metricProcessor = processor
        return self
