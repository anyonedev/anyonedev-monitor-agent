'''
Created on 2014-11-13

@author: hongye
'''

import subprocess

import psutil

from core import regist_monitor_source
from core.MetricValue import MultiMetricValue, SingleMetricValue
from core.MonitorSource import SampleMonitorSource


class PidProvider(object):
    _pid = None
    
    def __init__(self, pid=None):
        self._pid = pid
        
    def getPid(self):
        return self._pid
    
    
class CmdPidProvider(PidProvider):
    _cmd = None
    
    def __init__(self, cmd=None):
        self._cmd = cmd
        
    def getPid(self):
        p = subprocess.Popen(self._cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = ""
        for line in p.stdout.readlines():
            result = line
        p.wait()
        return int(result)

def pid_provider(pid):
    return PidProvider(pid)

def cmd_pid_provider(cmd):
    return CmdPidProvider(cmd)

class ProcessInfoMonitorSource(SampleMonitorSource):
    _pidProvider = None
    
    def __init__(self, pidProvider):
        self._pidProvider = pidProvider
    
    def sample(self, parms):
        pid = self._pidProvider.getPid()
        p = psutil.Process(pid)
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("pid", pid)
        metricValue.addMetricValue("name", p.name())
        metricValue.addMetricValue("create_time", p.create_time())
        metricValue.addMetricValue("status", p.status())
#        metricValue.addMetricValue("cwd", p.cwd())
        metricValue.addMetricValue("username", p.username())
        return metricValue

def process_info(monitorSourceName, pidProvider):
    monitorSource = ProcessInfoMonitorSource(pidProvider).monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ProcessMemoryMonitorSource(SampleMonitorSource):
    _pidProvider = None
    
    def __init__(self, pidProvider):
        self._pidProvider = pidProvider
    def sample(self, parms):
        pass

def process_memory(monitorSourceName, pidProvider):
    monitorSource = ProcessMemoryMonitorSource(pidProvider).monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ProcessIoCountersMonitorSource(SampleMonitorSource):
    _pidProvider = None
    
    def __init__(self, pidProvider):
        self._pidProvider = pidProvider
        
    def sample(self, parms):
        pid = self._pidProvider.getPid()
        p = psutil.Process(pid)
        io = p.io_counters()
        
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("read_count", io.read_count)
        metricValue.addMetricValue("write_count", io.write_count)
        metricValue.addMetricValue("read_bytes", io.read_bytes)
        metricValue.addMetricValue("write_bytes", io.write_bytes)
        return metricValue

def process_io_counters(monitorSourceName, pidProvider):
    monitorSource = ProcessIoCountersMonitorSource(pidProvider).monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ProcessConnectionsMonitorSource(SampleMonitorSource):
    _pidProvider = None
    _kind = "inet"
    
    def __init__(self, pidProvider):
        self._pidProvider = pidProvider
        
    def sample(self, parms):
        pid = self._pidProvider.getPid()
        p = psutil.Process(pid)
        conns = p.connections(self._kind)
        metricValue = SingleMetricValue(self.getMonitorSourceName(), "connections", conns)
        return metricValue

def process_connections(monitorSourceName, pidProvider):
    monitorSource = ProcessConnectionsMonitorSource(pidProvider).monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ProcessNumThreadsMonitorSource(SampleMonitorSource):
    _pidProvider = None
    
    def __init__(self, pidProvider):
        self._pidProvider = pidProvider
        
    def sample(self, parms):
        pid = self._pidProvider.getPid()
        p = psutil.Process(pid)
        threads = p.num_threads()
        metricValue = SingleMetricValue(self.getMonitorSourceName(), "num_threads", threads)
        return metricValue    

def process_num_threads(monitorSourceName, pidProvider):
    monitorSource = ProcessNumThreadsMonitorSource(pidProvider).monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ProcessCpuPercentMonitorSource(SampleMonitorSource):
    _pidProvider = None
    
    def __init__(self, pidProvider):
        self._pidProvider = pidProvider
        
    def sample(self, parms):
        pid = self._pidProvider.getPid()
        p = psutil.Process(pid)
        percent = p.cpu_percent()
        metricValue = SingleMetricValue(self.getMonitorSourceName(), "cpu_percent", percent)
        return metricValue   

def process_cpu_percent(monitorSourceName, pidProvider):
    monitorSource = ProcessCpuPercentMonitorSource(pidProvider).monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ProcessMemoryPercentMonitorSource(SampleMonitorSource):
    _pidProvider = None
    
    def __init__(self, pidProvider):
        self._pidProvider = pidProvider
        
    def sample(self, parms):
        pid = self._pidProvider.getPid()
        p = psutil.Process(pid)
        percent = p.memory_percent()
        metricValue = SingleMetricValue(self.getMonitorSourceName(), "memory_percent", percent)
        return metricValue   
    
def process_memory_percent(monitorSourceName, pidProvider):
    monitorSource = ProcessMemoryPercentMonitorSource(pidProvider).monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource
