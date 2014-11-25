'''
Created on 2014-11-13

@author: hongye
'''
import  json
import traceback

import tornado.httpserver
import tornado.ioloop
import tornado.web

from core import MetricValue, monitorSourceRegistry
from core.MetricProcessor import MetricProcessor
from core.MetricValue import MultiMetricValue, SingleMetricValue, \
    BatchMultiMetricValue, KeyedMultiMetricValue
from core.MonitorSource import SampleMonitorSource


class TornadoMetricProcessor(MetricProcessor):
    pass

class IndexHandler(tornado.web.RequestHandler):   
    def get(self):
        name = self.get_argument('name')
        if name == None:
            return 
        monitorSource = monitorSourceRegistry.getByMonitorSourceName(name)
        if monitorSource == None:
            return 
        
        if isinstance(monitorSource, SampleMonitorSource):
            metricValue = monitorSource.sample(None)
            values = dict()
            values["monitorSourceName"] = metricValue.getMonitorSourceName()
            values["clientId"] = metricValue.getClientId()
            values["sampleTime"] = metricValue.getSampleTime()
            values["status"] = metricValue.getStatus()
            if isinstance(metricValue, MultiMetricValue):
                values["type"] = "MultiMetricValue"
                values["values"] = metricValue.getValues()
            elif isinstance(metricValue, BatchMultiMetricValue):
                values["type"] = "BatchMultiMetricValue"
                values["values"] = metricValue.getValues()
            elif isinstance(metricValue, KeyedMultiMetricValue):
                values["type"] = "KeyedMultiMetricValue"
                values["values"] = metricValue.getValues()
            elif isinstance(metricValue, SingleMetricValue):
                values["type"] = "SingleMetricValue"
                values["values"] = metricValue.getValues()
                
            try:
                content = json.dumps(values)
                print(content)
                self.write(content)
            except:
                print(traceback.print_stack())
    def write_error(self, status_code, **kwargs):   
        self.write("You caused a %d error." % status_code)
        
class HTTPJsonExportMetricProcessor(TornadoMetricProcessor):
    _port = 8888
    
    def start(self):
        app = tornado.web.Application(handlers=[(r"/sample", IndexHandler)])  
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

    def port(self, port):
        self._port = port
        return self
    
def http_json_export(port=8888):
    return HTTPJsonExportMetricProcessor().port(port)

if __name__ == '__main__':
    processor = HTTPJsonExportMetricProcessor()
    processor.start()
