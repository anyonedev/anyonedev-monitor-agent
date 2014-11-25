'''
Created on 2014-11-13

@author: hongye
'''

import os

from core import regist_monitor_source
from core.MetricValue import MultiMetricValue
from core.MonitorSource import SampleMonitorSource


class LoadAvgMonitorSource(SampleMonitorSource):
    def sample(self, parms):
        with open('/proc/loadavg') as f:
            line = f.readline() 
            load_avgs = [float(x) for x in line.split()[:3]]
            metricvalue = MultiMetricValue(self.getMonitorSourceName())
            metricvalue.addMetricValue("short_term", load_avgs[0])  # 1min
            metricvalue.addMetricValue("mediun_term", load_avgs[1]) # 5min
            metricvalue.addMetricValue("long_term", load_avgs[2])   # 15 min
            return metricvalue
        return None