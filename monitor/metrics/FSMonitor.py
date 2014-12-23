'''
文件系统监控源(监控目录的变化)
Create ON 2014-12-23
Author: liangzonghua
配置参数:
   name : 数据源名称
   monitor_dir : 监控目录
   recursive   : 是否监控子目录
   observer   :  观察者
返回:MultiMetricValue
    monitorSourceName: 监控源名称
    clientId
    sampleTime
    status 
    type : created,modified,deleted,moved
    monitor_dir
    src_path
    dest_path : type=moved才有
    is_directory
    atime,ctime,mtime,size:type ！=deleted才有
'''
from core.MonitorSource import ObserableMonitorSource
from core.MetricProcessor import MetricProcessor
from core.MetricValue import MultiMetricValue
from utils import MetricValueJSONUtils
from core import regist_monitor_source
from utils.Logger import info

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
class EventHandler(FileSystemEventHandler):
    _monitor_source = None
    
    def __init__(self,source):
        self._monitor_source = source
        
    def on_any_event(self, event):
        metricValue = MultiMetricValue(self._monitor_source.getMonitorSourceName())
        metricValue.addMetricValue("type", event.event_type)
        metricValue.addMetricValue("monitor_dir",self._monitor_source._monitor_dir)
        metricValue.addMetricValue("src_path", event.src_path)
        metricValue.addMetricValue("is_directory", event.is_directory)
        f = event.src_path
        if hasattr(event, "dest_path"):
            metricValue.addMetricValue("dest_path", event.dest_path)
            f = event.dest_path
        if os.path.exists(f):
            metricValue.addMetricValue("atime", os.path.getatime(f))
            metricValue.addMetricValue("ctime", os.path.getctime(f))
            metricValue.addMetricValue("mtime", os.path.getmtime(f))
            metricValue.addMetricValue("size", os.path.getsize(f))
        self._monitor_source.notify(metricValue)
        
class DirectoryMonitorSource(ObserableMonitorSource):
    _monitor_dir = "."
    _recursive = True
    def __init__(self,name,monitor_dir,recursive=True):
        self._monitorSourceName = name
        self._monitor_dir = monitor_dir
        self._recursive = recursive
            
    def start(self):
        if not os.path.exists(self._monitor_dir):
            os.makedirs(self._monitor_dir)
            info("create monitor dir:"+self._monitor_dir)
        self._observer = Observer()
        self._observer.schedule(EventHandler(self), self._monitor_dir, recursive=self._recursive)
        self._observer.start()
        ObserableMonitorSource.start(self)
        info("monitor dir start:"+self._monitor_dir)
        
    def stop(self):
        if hasattr(self, "_observer") and self._observer!=None:
            self._observer.stop() 
            self._observer = None
        ObserableMonitorSource.stop(self)
        info("monitor dir stop:"+self._monitor_dir)

def directory_change(name,monitor_dir,is_recursive=True,observers=[]):
    monitorSource = DirectoryMonitorSource(name,monitor_dir,is_recursive)
    for o in observers:
        monitorSource.addObserver(o)
    regist_monitor_source(monitorSource)
    return monitorSource


#test
class LogObserver(MetricProcessor):
    def onNotify(self, metricValue):
        info(MetricValueJSONUtils.toJSON(metricValue))
if __name__ == "__main__":
    monitorSource = directory_change("on_directory_change", "D:/test", True,[LogObserver()])
