'''
监控数据发送至Graphite服务器(默认Graphite使用carbon存储数据)
Created on 2014-11-13
配置from monitor.config.graphiteSender
    Carbon_LineReceiverHost : 接收服务器地址，默认localhost
    Carbon_LineReceiverPort : 端口号,默认2003
    Carbon_LineReceiverProtocol : 协议，默认tcp
@author: hongye,liangzonghua
'''
from monitor.core.MetricProcessor import MetricProcessor
from monitor.config import config
from monitor.utils.Logger import info, warn
from time import time

import socket
import threading
from core.MetricValue import SingleMetricValue, MultiMetricValue, \
    BatchMultiMetricValue, KeyedMultiMetricValue
    
    
GRAPHITE_LINE_FORMAT = "%s %f %d"
class GraphiteSenderMetricProcessor(MetricProcessor):
    _data = None
    def start(self):
        self._data = dict()
        self._data["host"] = config.graphiteSender.get("Carbon_LineReceiverHost")
        self._data["port"] = config.graphiteSender.get("Carbon_LineReceiverPort")
        self._data["protocol"] = config.graphiteSender.get("Carbon_LineReceiverProtocol")
        self._data["lock"] = threading.Lock()
        self._data["sock"] = None
        self._data["last_connect_time"] = 0   
        print(self._data)
        self._carbon_reconnect(self._data)
        
    def stop(self):
        if self._data != None and self._data["sock"] != None:
            self._data["sock"].close()
            self._data["sock"] = None
        
    def process(self, metricValue):
        if metricValue == None:
            return;
        sampleTime = metricValue.getSampleTime() / 1000
        clientId = metricValue.getClientId();
        monitorSourceName = metricValue.getMonitorSourceName()
        
        prePath = clientId + "." + monitorSourceName + "."
        if isinstance(metricValue, SingleMetricValue):
            key = metricValue.getMetricName()
            value = metricValue.getMetricValue()
            self._write_data(self._data,GRAPHITE_LINE_FORMAT % (prePath + key, value, sampleTime) + "\n")
        elif isinstance(metricValue, MultiMetricValue):
            values = metricValue.getValues()
            lines = []
            for key, value in values.items():
                lines.append(GRAPHITE_LINE_FORMAT % (prePath + key, value, sampleTime))
            self._write_data(self._data, "\n".join(lines))
        elif isinstance(metricValue, BatchMultiMetricValue):
            values = metricValue.getValues()
            length = len(values)
            index = 0
            lines = []
            while(index < length):
                multiMetricValue = values[index]
                batchPrePath = prePath + str(index) + "."
                if multiMetricValue.getValues() == None:
                    continue
                for key, value in multiMetricValue.getValues().items():
                    line = GRAPHITE_LINE_FORMAT % (batchPrePath + key, value, sampleTime)
                    lines.append(line)
                index = index + 1
            self._write_data(self._data, "\n".join(lines))
        elif isinstance(metricValue, KeyedMultiMetricValue):
            values = metricValue.getValues()
            lines = []
            for keyed, multiMetricValue in values.items():
                keyedPrePath = prePath + str(keyed) + "."
                for key, value in multiMetricValue.getValues().items():
                    line = GRAPHITE_LINE_FORMAT % (keyedPrePath + key, value, sampleTime)
                    lines.append(line)
            self._write_data(self._data, "\n".join(lines))
        else: 
            warn("未知MetricValue类型:" + str(metricValue.__class__))    
            
    def _write_data(self, data, line):
        print(line)
        result = False
        data['lock'].acquire()
        try:
            if data["protocol"].lower() == 'tcp':
                self._carbon_reconnect(data)
                data['sock'].sendall(line.encode("utf-8"))
            else:  # send message to via UDP to the line receiver .
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(line.encode("utf-8"), (data["host"], data["port"]))
            result = True
        except socket.error as e:
            data['sock'] = None
            self._carbon_reconnect(data)
            if isinstance(e.args, tuple):
                warn('graphite_sender: socket error %d' % e[0])
            else:
                warn('graphite_sender: socket error')
        except Exception as e:
                warn('graphite_sender error:sending data failure:' + str(e))

        data['lock'].release()
        return result
       
    def _carbon_reconnect(self,data):
        '''only protocol == tcp need reconnect'''
        result = False
        try:
            if str(data["protocol"]).lower() == 'tcp':
                if data["sock"] == None:
                    data['last_connect_time'] = 0
                # only attempt reconnect every 10 seconds if protocol of type TCP
                now = time()
                if now - data['last_connect_time'] < 10:
                    result = True
                else:
                    data['last_connect_time'] = now
                    info('connecting to %s:%s' % (data['host'], data['port']))
                    try:
                        data['sock'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        data['sock'].connect((data["host"], data["port"]))
                        result = True
                    except:
                        result = False
                        warn('error connecting socket: %s:%d' % (data["host"], data["port"]))
            else: # we're protocol does not == tcp. we will send data via udp/SOCK_DGRAM call.
                result = True
            return result 
        except Exception as e:
            print(e)
            warn('error connecting socket: %s:%d' % (data["host"], data["port"]))
            return False
