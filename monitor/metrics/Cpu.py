'''
Created on 2014-11-12

@author: hongye
'''
import psutil

from core import regist_monitor_source
from core.MetricValue import MultiMetricValue, SingleMetricValue
from core.MonitorSource import SampleMonitorSource


class CpuTimesMonitorSource(SampleMonitorSource):
    def sample(self, parms):
        cpu = psutil.cpu_times()
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("user", cpu.user)
        metricValue.addMetricValue("system", cpu.system)
        metricValue.addMetricValue("idle", cpu.idle)
        return metricValue

class CpuPercentMonitorSource(SampleMonitorSource):
    interval = None
    def sample(self, parms):
        value = psutil.cpu_percent(self.interval)
        return SingleMetricValue(self.getMonitorSourceName(), "cpu_percent", value)

class CpuTimesPercentMonitorSource(SampleMonitorSource):
    _interval = None
    
    def sample(self, parms):
        cpu = psutil.cpu_times_percent(self._interval)
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("user", cpu.user)
        metricValue.addMetricValue("system", cpu.system)
        metricValue.addMetricValue("idle", cpu.idle)
        return metricValue
    
    def interval(self, interval):
        self._interval = interval

def cpu_percent(monitorSourceName):
    monitorSource = CpuPercentMonitorSource().monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

def cpu_times_percent(monitorSourceName):
    monitorSource = CpuTimesPercentMonitorSource().monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource
    
def cpu_times(monitorSourceName):
    monitorSource = CpuTimesMonitorSource().monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource
