'''
Created on 2014-11-12

@author: hongye
'''

import psutil

from core import regist_monitor_source
from core.MetricValue import MultiMetricValue, BatchMultiMetricValue, \
    KeyedMultiMetricValue
from core.MonitorSource import SampleMonitorSource


class DiskPartitionsMonitorSource(SampleMonitorSource):

    def sample(self, parms):
        partitions = psutil.disk_partitions()
        metricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for p in partitions:
            value = dict()
            value["device"] = p.device
            value["mountpoint"] = p.mountpoint
            value["fstype"] = p.fstype
            value["opts"] = p.opts
            metricValue.addMetricValue(value)
        return metricValue

class DiskUsageMonitorSource(SampleMonitorSource):
    path = "/"
    
    def sample(self, parms):
        usage = psutil.disk_usage(self.path)
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("total", usage.total)
        metricValue.addMetricValue("used", usage.used)
        metricValue.addMetricValue("free", usage.free)
        metricValue.addMetricValue("percent", usage.percent)
        return metricValue
    
    def path(self, path):
        self.path = path
        return self

class DiskIoCountersMonitorSource(SampleMonitorSource):
    _perdisk = False
    def sample(self, parms):
        io = psutil.disk_io_counters(self._perdisk)
        if self._perdisk:
            metricValue = KeyedMultiMetricValue(self.getMonitorSourceName())
            for (k, v) in io.items():
                value = dict()
                value["read_count"] = v.read_count
                value["write_count"] = v.write_count
                value["read_bytes"] = v.read_bytes
                value["write_bytes"] = v.write_bytes
                value["read_time"] = v.read_time
                value["write_time"] = v.write_time
                metricValue.addMetricValue(k, value)
            return metricValue
        else:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("read_count", io.read_count)
            metricValue.addMetricValue("write_count", io.write_count)
            metricValue.addMetricValue("read_bytes", io.read_bytes)
            metricValue.addMetricValue("write_bytes", io.write_bytes)
            metricValue.addMetricValue("read_time", io.read_time)
            metricValue.addMetricValue("write_time", io.write_time)
            return metricValue
    
    def perdisk(self, perdisk):
        self._perdisk = perdisk
        return self

def disk_partitions(monitorSourceName):
    monitorSource = DiskPartitionsMonitorSource().monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

def disk_usage(monitorSourceName, path="/"):
    monitorSource = DiskUsageMonitorSource().monitorSourceName(monitorSourceName).path(path)
    regist_monitor_source(monitorSource)
    return monitorSource

def disk_io_counters(monitorSourceName, perdisk=False):
    monitorSource = DiskIoCountersMonitorSource().monitorSourceName(monitorSourceName).perdisk(perdisk)
    regist_monitor_source(monitorSource)
    return monitorSource

