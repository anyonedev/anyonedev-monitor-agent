'''
Created on 2014-11-15

@author: hongye,liangzonghua
'''
from core.MonitorSource import SampleMonitorSource
from core.MetricValue import MultiMetricValue, KO 
from pysnmp.entity.rfc3413.oneliner import cmdgen
from monitor.utils.Logger import warn
from utils import MetricValueJSONUtils
from core import regist_monitor_source


class SNMPMonitorSource(SampleMonitorSource):
    _cmdGenerator = None
    _host = "127.0.0.1"
    _port = 161
    _community_data_name = "public"
    _sample_varnames = []
    
    def __init__(self,host="127.0.0.1",port=161,community_data_name="public",sample_varnames=[]):
        self._host = host
        self._port = port
        self._community_data_name = community_data_name
        self._sample_varnames = sample_varnames
    
    def createMibVariables(self,names):
        return (cmdgen.MibVariable("SNMPv2-MIB",name,0) for name in names)
    
    def sample(self, parms):
        if len(self._sample_varnames) is 0:
            warn("没有配置mib name")
            return MultiMetricValue(self.getMonitorSourceName())
        if self._cmdGenerator is None:
            self._cmdGenerator = cmdgen.CommandGenerator()
        result = MultiMetricValue(self.getMonitorSourceName())
        mibVariables = self.createMibVariables(self._sample_varnames)
        errorIndication,errorStatus,errorIndex,varBinds = self._cmdGenerator.getCmd(
            cmdgen.CommunityData(self._community_data_name),
            cmdgen.UdpTransportTarget((self._host,self._port)),
            *mibVariables,
            lookupNames=True,
            lookupValues=True
        )
        if errorIndication or errorStatus or errorIndex:
            result.status(KO)
            result.addMetricValue("errorIndication", errorIndication.__dict__)
            result.addMetricValue("errorStatus", errorStatus)
            result.addMetricValue("errorIndex", errorIndex)
        else:
            for name, val in varBinds:
                result.addMetricValue(name.prettyPrint(), val.prettyPrint())
        return result
    
def snmp_monitor_source(monitorSourceName="",host="127.0.0.1",port="161",community_data_name="public",sample_varnames=[]):
    monitorSource = SNMPMonitorSource(host,port,community_data_name,sample_varnames)
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class OracleSNMPMonitorSource(SNMPMonitorSource):
    pass

#for test
if __name__ == "__main__":
    rs = snmp_monitor_source(sample_varnames=["sysName","sysUpTime","sysContact"]).monitorSourceName("snmp").sample(None)
    print(MetricValueJSONUtils.toJSON(rs))