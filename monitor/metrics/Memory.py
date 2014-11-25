'''
Created on 2014-11-12

@author: hongye
'''

import psutil

from core import regist_monitor_source
from core.MetricValue import MultiMetricValue
from core.MonitorSource import SampleMonitorSource


class VirtualMemoryMonitorSource(SampleMonitorSource):
    
    def sample(self, parms):
        mem = psutil.virtual_memory()
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("total", mem.total)
        metricValue.addMetricValue("available", mem.available)
        metricValue.addMetricValue("percent", mem.percent)
        metricValue.addMetricValue("used", mem.used)
        metricValue.addMetricValue("free", mem.free)
        return metricValue

class SwapMemoryMonitorSource(SampleMonitorSource):
    def sample(self, parms):
        mem = psutil.swap_memory()
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("total", mem.total)
        metricValue.addMetricValue("percent", mem.percent)
        metricValue.addMetricValue("used", mem.used)
        metricValue.addMetricValue("free", mem.free)
        metricValue.addMetricValue("sin", mem.sin)
        metricValue.addMetricValue("sout", mem.sout)
        return metricValue

def virtual_memory(monitorSourceName):
    monitorSource = VirtualMemoryMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

def swap_memory(monitorSourceName):
    monitorSource = SwapMemoryMonitorSource().monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource
