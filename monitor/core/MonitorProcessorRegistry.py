'''
Created on 2014-11-12

@author: hongye
'''

class MonitorProcessorRegistry(object):
    processors = dict()
    
    def registMonitorProcessor(self, name, metricProcessor):
        if self.processors.get(name) != None:
            raise "处理器已经存"
        metricProcessor.start()
        self.processors[name] = metricProcessor
    
    def unregistMonitorProcessor(self, name):
        processor = self.processors.get(name)
        if processor == None:
            return
        processor.stop()
        self.processors.pop(name)
