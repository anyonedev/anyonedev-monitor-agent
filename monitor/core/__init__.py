from apscheduler.scheduler import Scheduler

from core.MetricProcessor import MetricProcessor
from core.MonitorProcessorRegistry import MonitorProcessorRegistry
from core.MonitorSource import MonitorSource 
from core.MonitorSourceMatcher import MonitorSourceMatcher
from core.MonitorSourceMatcher import MonitorSourceNameMatcher
from core.MonitorSourceRegistry import MonitorSourceRegistry


monitorSourceRegistry = MonitorSourceRegistry()
schedudler = Scheduler(daemonic=False)
schedudler.start();

monitorProcessorRegistry = MonitorProcessorRegistry()

def regist_monitor_source(monitorSource:MonitorSource):
    monitorSourceRegistry.registMonitorSource(monitorSource)

def regist_metric_processor(name, metricProcessor):
    monitorProcessorRegistry.registMonitorProcessor(name, metricProcessor)


def monitor_source_name_matcher(monitorSourceName):
    return MonitorSourceNameMatcher(monitorSourceName)
