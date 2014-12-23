'''
监控指标值HTTP导出处理器
Created on 2014-11-13
使用Tornado作为http服务器，支持http请求采样信息
参数:
    name : 需要采样的监控源名称，必须是可采样的监控源
返回: json数据格式
    success : 是否采样成功
    message : 信息(如success=false的原因)
    
    monitorSourceName: 监控源名称
    clientId : 节点编号
    sampleTime: 采样时间戳
    status : 状态
    values : 采样值
        SingleMetricValue : dict
        MultiMetricValue  : dict
        BatchMultiMetricValue: array[dict]
        KeyedMultiMetricValue: dict{(keyed,dict)}
    
@author: hongye,liangzonghua
'''
import  json
import traceback

import tornado.httpserver
import tornado.ioloop
import tornado.web

from core import monitorSourceRegistry
from core.MetricProcessor import MetricProcessor
from core.MetricValue import MultiMetricValue, SingleMetricValue, \
    BatchMultiMetricValue, KeyedMultiMetricValue
from core.MonitorSource import SampleMonitorSource
from metrics.Cpu import cpu_percent
from config.config import httpExportConfig

IS_ALLOW_CORS = httpExportConfig.get("allow_cors")
PORT = httpExportConfig.get("port")
class TornadoMetricProcessor(MetricProcessor):
    pass

class IndexHandler(tornado.web.RequestHandler): 
    
    def _handle(self):
        name = self.get_argument('name',default=None)
        if name == None:
            result = json.dumps({"success":False,"message":"missing 'name' param"})
            self.write(result)
            return 
        monitorSource = monitorSourceRegistry.getByMonitorSourceName(name)
        if monitorSource == None:
            result = json.dumps({"success":False,"message":"un-registry monitorSource","monitorSourceName":name})
            self.write(result)
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
                values["values"] = [multi.getValues() for multi in metricValue.getValues()]
            elif isinstance(metricValue, KeyedMultiMetricValue):
                values["type"] = "KeyedMultiMetricValue"
                if metricValue.getValues () != None:
                    vs = dict()
                    for keyed,multi in metricValue.getValues().items():
                        if multi != None:
                            vs[keyed] = multi.getValues()
                    values["values"] = vs
            elif isinstance(metricValue, SingleMetricValue):
                values["type"] = "SingleMetricValue"
                values["values"] = {metricValue.getMetricName():metricValue.getMetricValue()}
            try:
                values["success"] = True
                values["message"] = "sample success"
                content = json.dumps(values)
                print(content)
                self.write(content)
            except:
                result = json.dumps({"success":False,"message":"unknow exception"})
                self.write(result)
                print(traceback.print_stack())
        else:
            result = json.dumps({"success":False,"message":"is not instance of SampleMonitorSource","monitorSourceName":name})
            self.write(result)
    
    def prepare(self):
        if IS_ALLOW_CORS:
            #允许请求跨域的设置
            self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
            self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
            self.set_header("Access-Control-Allow-Origin", "*") 
        
    def options(self, *args, **kwargs):
        #call prepare to allow Cross-Origin
        pass
        
    def get(self, *args, **kwargs):
        self._handle()
    def post(self, *args, **kwargs):
        self._handle()
    def put(self, *args, **kwargs):
        self._handle()
    def delete(self, *args, **kwargs):
        self._handle()
    
    def write_error(self, status_code, **kwargs):   
        self.write("You caused a %d error." % status_code)
        
class HTTPJsonExportMetricProcessor(TornadoMetricProcessor):
    _port = PORT
    
    def start(self):
        try:
            app = tornado.web.Application(handlers=[(r"/sample", IndexHandler)])
            http_server = tornado.httpserver.HTTPServer(app)
            http_server.listen(self._port)
            #app.listen("8888", "0.0.0.0")
            tornado.ioloop.IOLoop.instance().start()
        except Exception as ex:
            raise ex

    def port(self, port):
        self._port = port
        return self
    
def http_json_export(port=PORT):
    return HTTPJsonExportMetricProcessor().port(port)


# for test call  
if __name__ == '__main__':
    cpu_percent("cpu_percent")
    processor = http_json_export()
    processor.start()
