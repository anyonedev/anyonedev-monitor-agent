'''
网卡信息采集监控源

Create On: 2014-12-19
@author:  liangzonghua

注意:
    1.对于绑定多个IP地址的网口只采集第一个IP地址信息
    2.采集数据包括link，inet，inet6
    3.返回类型是KeyedMultiMetricValue
样例: 
    windows下: 
    {"monitorSourceName": "netiface", "clientId": "outworker", "values": {"{9C515D91-ED07-433A-9685-BCF4F9707D58}": {"link_addr": "00:00:00:00:00:00:00:e0", "inet6_addr": "fe80::5efe:192.168.0.115%24"}, "{5CAB13B5-72E3-4AF1-A81B-9D7C791E5F4C}": {"link_addr": "00:00:00:00:00:00:00:e0"}, "{9ED8A51B-B13B-4E58-8B02-E6373D0535E7}": {"link_addr": "00:00:00:00:00:00:00:e0"}, "{BA376B5F-AA57-4805-8C9B-91565886CCEE}": {"link_addr": "30:14:4a:81:72:24", "inet_addr": "192.168.0.115", "inet_broadcast": "192.168.0.255", "inet6_addr": "fe80::5116:33dd:2f9c:6bc5%13", "inet_netmask": "255.255.255.0"}, "{E6B02B57-EE01-4428-9A9C-CA52CF0847DE}": {"link_addr": "00:ff:e6:b0:2b:57", "inet_addr": "169.254.135.19", "inet6_addr": "fe80::20ea:1c05:795c:8713%15"}, "{28EE3503-42C7-4252-8B52-3E01C2B2C39F}": {"link_addr": "00:00:00:00:00:00:00:e0"}, "{A6157757-9518-441B-BC4F-FF427C3C222A}": {"link_addr": "08:00:27:00:f4:1f", "inet_addr": "169.254.51.25", "inet_broadcast": "169.254.255.255", "inet6_addr": "fe80::c837:3d61:eac4:3319%19", "inet_netmask": "255.255.0.0"}, "{54F229F5-1BA7-488D-B096-DD33CFA8FB24}": {"link_addr": "50:af:73:1e:ed:26", "inet_addr": "169.254.63.91", "inet6_addr": "fe80::6594:ad93:ca59:3f5b%11"}, "{83D2A0B7-046A-4EFA-BFC9-FA5540CEA257}": {"link_addr": "00:00:00:00:00:00:00:e0"}, "{846EE342-7039-11DE-9D20-806E6F6E6963}": {"link_addr": "", "inet_addr": "127.0.0.1", "inet_broadcast": "127.255.255.255", "inet6_addr": "::1", "inet_netmask": "255.0.0.0"}, "{E5AC7861-7359-44AB-ABF2-99377FFE07A5}": {"link_addr": "22:14:4a:81:72:24", "inet_addr": "169.254.204.106", "inet6_addr": "fe80::c836:6a2:c5f0:cc6a%14"}, "{F4D29529-5373-44D1-A85E-D97D5696F8CB}": {"link_addr": "00:00:00:00:00:00:00:e0", "inet6_addr": "fe80::e0:0:0:0%12"}}, "sampleTime": 1418980263322}


'''
from monitor.core.MonitorSource import SampleMonitorSource
from monitor.core.MetricValue import KeyedMultiMetricValue, MultiMetricValue
import netifaces
from monitor.core import regist_monitor_source
from monitor.utils import MetricValueJSONUtils

class NetIfaceMonitorSource(SampleMonitorSource):
    
    def sample(self, parms):
        ifaceNames = netifaces.interfaces()
        result = KeyedMultiMetricValue(self.getMonitorSourceName())
        for iface in ifaceNames:
            multi = MultiMetricValue(self.getMonitorSourceName())
            info = netifaces.ifaddresses(iface)
            t = info.get(netifaces.AF_LINK)
            if t != None:
                for key,value in t[0].items():
                    multi.addMetricValue("link_"+str(key), value)
            t = info.get(netifaces.AF_INET)
            if t != None:
                for key,value in t[0].items():
                    multi.addMetricValue("inet_"+str(key), value)
            t = info.get(netifaces.AF_INET6)
            if t != None:
                for key,value in t[0].items():
                    multi.addMetricValue("inet6_"+str(key), value)
            if multi.getValues() == None:
                continue
            else:
                result.addMetricValue(iface, multi)
        return result 

def netiface_monitor_source(monitorSourceName):
    monitorSource = NetIfaceMonitorSource().monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource
    
if __name__ == "__main__":
    try:
        metricValue = netiface_monitor_source("netiface").sample(None)
        print(MetricValueJSONUtils.toJSON(metricValue))
        print("OK.")
    except Exception as ex:
        raise ex