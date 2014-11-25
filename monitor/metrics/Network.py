'''
Created on 2014-11-12

@author: hongye
'''

import psutil

from core import regist_monitor_source
from core.MetricValue import MultiMetricValue, BatchMultiMetricValue, \
    KeyedMultiMetricValue
from core.MonitorSource import SampleMonitorSource


class NetIoCountersMonitorSource(SampleMonitorSource):
    _pernic = False
    
    def pernic(self, pernic=False):
        self._pernic = pernic
        return self
    
    def sample(self, parms):
        nic = psutil.net_io_counters(pernic=self._pernic)
        if self._pernic == True:
            metricValue = KeyedMultiMetricValue(self.getMonitorSourceName())
            for (k, v) in nic.items():
                value = dict()
                value["bytes_sent"] = v.bytes_sent
                value["bytes_recv"] = v.bytes_recv
                value["packets_sent"] = v.packets_sent
                value["packets_recv"] = v.packets_recv
                value["errin"] = v.errin
                value["errout"] = v.errout
                value["dropin"] = v.dropin
                value["dropout"] = v.dropout
                metricValue.addMetricValue(k, value)
            return metricValue    
        else:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("bytes_sent", nic.bytes_sent)
            metricValue.addMetricValue("bytes_recv", nic.bytes_recv)
            metricValue.addMetricValue("packets_sent", nic.packets_sent)
            metricValue.addMetricValue("packets_recv", nic.packets_recv)
            metricValue.addMetricValue("errin", nic.errin)
            metricValue.addMetricValue("errout", nic.errout)
            metricValue.addMetricValue("dropin", nic.dropin)
            metricValue.addMetricValue("dropout", nic.dropout)
            return metricValue

NET_CONNECTION_KIND_INET = "inet"
NET_CONNECTION_KIND_INET4 = "inet4"
NET_CONNECTION_KIND_INET6 = "inet6"
NET_CONNECTION_KIND_TCP = "tcp"
NET_CONNECTION_KIND_TCP4 = "tcp4"
NET_CONNECTION_KIND_TCP6 = "tcp6"
NET_CONNECTION_KIND_UDP = "udp"
NET_CONNECTION_KIND_UDP4 = "udp4"
NET_CONNECTION_KIND_UDP6 = "udp6"
NET_CONNECTION_KIND_UNIX = "unix"
NET_CONNECTION_KIND_ALL = "all"

class NetConnectionsMonitorSource(SampleMonitorSource):
    _kind = NET_CONNECTION_KIND_INET
    def kind(self, kind=NET_CONNECTION_KIND_INET):
        self._kind = kind
        return self
    
    def sample(self, parms):
        conns = psutil.net_connections(self._kind)
        metricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for conn in conns:
            value = dict()
            value["fd"] = conn.fd
            value["family"] = conn.family
            value["type"] = conn.type
#             value["laddr"] = conn.laddr
#             value["raddr"] = conn.raddr
            value["status"] = conn.status
            value["pid"] = conn.pid
            metricValue.addMetricValue(value)
        return metricValue

def net_io_counters(monitorSourceName, pernic=False):
    monitorSource = NetIoCountersMonitorSource().monitorSourceName(monitorSourceName).pernic(pernic)
    regist_monitor_source(monitorSource)
    return monitorSource

def net_connections(monitorSourceName, kind=NET_CONNECTION_KIND_INET):
    monitorSource = NetConnectionsMonitorSource().monitorSourceName(monitorSourceName).kind(kind)
    regist_monitor_source(monitorSource)
    return monitorSource
