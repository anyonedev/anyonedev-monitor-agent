'''
Created on 2014-11-12

@author: hongye
'''
from core.MetricProcessor import MetricProcessor


class ChainMetricProcessor(MetricProcessor):
    processors = []
    
    def start(self):
        for p in self.processors:
            p.start()

    def process(self, metricValue):
        for p in self.processors:
            p.process(metricValue)
    
    def processor(self, p):
        self.processors.append(p)
        return self
    
    def stop(self):
        for p in self.processors:
            p.stop()