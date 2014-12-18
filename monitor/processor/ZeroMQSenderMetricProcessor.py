'''
Created on 2014-11-18
监控信息发送至zeromq
配置属性:
    host : 服务器地址
    port : 端口号,
    type : 发送类型 ，默认zmq.PUB
    destination : 发动地址，默认DEFAULT
消息格式:数组
    [destination,clientId,monitorSourceName,sampleTime,metricValue(JOSON)]
@author: hongye,liangzonghua
'''
from monitor.core.MetricProcessor import MetricProcessor
from monitor.utils.Logger import info,warn
from time import time
import zmq
import threading
from logging import warning
from monitor.utils.MetricValueJSONUtils import  toJSON


class ZeroMQSenderMetricProcessor(MetricProcessor):
    _ctx = zmq.Context()
    _host = None
    _port = None
    _protocol = None
    _type = None
    _time = 0
    _lock = None
    _destination = None

    _client = None
    def __init__(self,host,port,protocol="tcp",type=zmq.PUB,destination="DEFAULT"):
        self._host = host
        self._port = port
        self._protocol = protocol
        self._type = type
        self._destination = destination
        self._time = 0
        self._lock = threading.RLock(True)
        
    def _zmq_connect(self):
        self._lock.acquire(True)
        try:
            if self._client == None or (self._protocol == "tcp"):
                now = time()
                #reflash tcp connect every 10 seconds
                if self._protocol == "tcp" and now - self._time <10:
                    return
                self._time = now
                info("connect to zeromq...")
                self._client = self._ctx.socket(self._type)
                if self._type == zmq.PUB:
                    self._client.bind("%s://%s:%d"%(self._protocol,self._host,self._port))
                elif self._type == zmq.REQ:
                    self._client.connect("%s://%s:%d"%(self._protocol,self._host,self._port))
                else:
                    pass
                info("connect OK.")
        except Exception as e:
            warn(e)
        finally:
            self._lock.release()
            
    def start(self):
        self._zmq_connect();
        info("zero sender start OK.")
    
    def stop(self):
        self._lock.acquire(True, -1)
        if self._client != None:
            self._client.close()
            self._client = None
        self._lock.release()
    
    def process(self, metricValue):
        self._lock.acquire(True)
        try:
            sampleTime = metricValue.getSampleTime()
            monitorSourceName = metricValue.getMonitorSourceName()
            clientId = metricValue.getClientId()
            self._zmq_connect();
            msg_body = toJSON(metricValue)
            self._client.send_multipart([self._destination.encode("utf-8"),
                                         clientId.encode("utf-8"),
                                         monitorSourceName.encode("utf-8"),
                                         str(sampleTime).encode("utf-8"),
                                         msg_body.encode("utf-8")
                                        ])
        except Exception as ex:
            warn(ex)
        finally:
            self._lock.release()
