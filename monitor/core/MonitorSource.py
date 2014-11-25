'''
Created on 2014-11-12

@author: hongye
'''
class MonitorSource(object):
    _monitorSourceName = ""
    
    def getMonitorSourceName(self):
        return self._monitorSourceName
    
    def monitorSourceName(self, name):
        self._monitorSourceName = name
        return self
    
    def start(self):
        pass
    def stop(self):
        pass
    def fail(self):
        pass
'''
sample 返回parms
'''
class SampleMonitorSource(MonitorSource):
    
    def sample(self, parms):
        pass

class MonitorSourceObserver(object):
    
    def onNotify(self, MetricValue):
        pass
    
class ObserableMonitorSource(MonitorSource):
    observers = []
    
    def addObserver(self, observer:MonitorSourceObserver):
        self.observers.append(observer)
    
    def notify(self, metricValue):
        for observer in self.observers:
            observer.onNotify(metricValue)
            
    def removeObserver(self, observer:MonitorSourceObserver):
        self.observers.remove(observer)

