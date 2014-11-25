'''
Created on 2014-11-12

@author: hongye
'''

class MonitorSourceMatcher(object):
    
    def match(self, monitorSource):
        pass

class MonitorSourceNameMatcher(MonitorSourceMatcher):
    name = ""
    def __init__(self, name):
        self.name = name
    
    def match(self, monitorSource):
        if self.name == monitorSource.getMonitorSourceName():
            return True
        return False
        
