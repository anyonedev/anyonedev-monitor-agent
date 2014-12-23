'''
监控linux目录变化(可观察的监控源)
Create on : 2014-12-23
Author：liangzonghua
'''
from core.MonitorSource import ObserableMonitorSource
from core.MetricValue import MultiMetricValue
from core import regist_monitor_source
from utils.Logger import info
import os
import pyinotify

class DiectoryChangleHanlder(pyinotify.ProcessEvent):
    _monitor_source = None
    def __init__(self,ms):
        self._monitor_source = ms
    
    def process_default(self,event):
        f = event.pathname
        info(event.maskname+":"+f)
        metricValue = MultiMetricValue(self._monitor_source.getMonitorSourceName())
        metricValue.addMetricValue("type", event.maskname)
        metricValue.addMetricValue("monitor_path",event.path)
        metricValue.addMetricValue("monitor_file",event.file)
        metricValue.addMetricValue("is_directory",event.dir)
        if hasattr(event, "src_pathname"):
            metricValue.addMetricValue("src_pathname",event.src_pathname)
        if os.path.exists(f):
            metricValue.addMetricValue("atime", os.path.getatime(f))
            metricValue.addMetricValue("ctime", os.path.getctime(f))
            metricValue.addMetricValue("mtime", os.path.getmtime(f))
            metricValue.addMetricValue("size",  os.path.getsize(f))
        self._monitor_source.notify(metricValue)

DEFAULT_MONITOR_MASK = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM    
class LiuxDirectoryMonitorSource(ObserableMonitorSource):
    _monitor_dir = "."
    _monitor_mask= DEFAULT_MONITOR_MASK
    _is_rec = True
    def __init__(self,monitorSourceName, directory=None, mask=DEFAULT_MONITOR_MASK, rec = True):
        self.monitorSourceName(monitorSourceName)
        if dir != None:
            self._monitor_dir = directory
        if mask != None:
            self._monitor_mask = mask
        self._is_rec = rec
            
    def start(self):
        ObserableMonitorSource.start(self)
        if not os.path.exists(self._monitor_dir):
            os.makedirs(self._monitor_dir,exist_ok=True)
            info("create monitor dir:%s"%(self._monitor_dir))
        
        wm= pyinotify.WatchManager() 
        eventHandler= DiectoryChangleHanlder(self)
        self._notifier= pyinotify.Notifier(wm, eventHandler)
        wm.add_watch(self._monitor_dir, self._monitor_mask,self._is_rec)
        info('now starting monitor: %s'%(self._monitor_dir))
        while True:
            try:
                if self._notifier.is_alive():
                    self._notifier.process_events()
                    if self._notifier.check_events():
                        self._notifier.read_events()
                else:
                    break
            except KeyboardInterrupt:
                self.stop()
                break
    
    def stop(self):
        if hasattr(self, "_notifier") and self._notifier != None:
            self._notifier.stop()
        ObserableMonitorSource.stop(self)
        
def linux_dir_stat(name="linux_dir_stat",monitor_dir=".",rec=True,mask=DEFAULT_MONITOR_MASK):
    monitorSource = LiuxDirectoryMonitorSource(monitorSourceName=name,directory=monitor_dir,mask=mask,rec=rec)
    regist_monitor_source(monitorSource)
    return monitorSource