'''
Created on 2014-11-12

@author: hongye
'''

class MonitorSourceRegistry(object):
    monitorSources = dict()
    
    def getByMonitorSourceMatcher(self, matcher):
        results = []
        for (k, v) in self.monitorSources.items():
            if matcher.match(v):
                results.append(v)
        return results
    
    def getByMonitorSourceName(self,name):
        for (k, v) in self.monitorSources.items():
            if k == name:
                return v
        return None
    
    def registMonitorSource(self, monitorSource):
        name = monitorSource.getMonitorSourceName()
        if self.monitorSources.get(name) != None:
            raise "monitor source already exists!"
        monitorSource.start()
        self.monitorSources[name] = monitorSource
    
    
    def unregistMonitorSource(self, monitorSource):
        name = monitorSource.getMonitorSourceName()
        if self.monitorSources.get(name) != None:
            monitorSource.stop()
            self.monitorSources.remove(monitorSource)
