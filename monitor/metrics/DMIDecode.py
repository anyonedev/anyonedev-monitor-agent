from core import regist_monitor_source
from core.MetricValue import MultiMetricValue
from core.MonitorSource import SampleMonitorSource


TYPE = {
    0:  'bios',
    1:  'system',
    2:  'base board',
    3:  'chassis',
    4:  'processor',
    7:  'cache',
    8:  'port connector',
    9:  'system slot',
    10: 'on board device',
    11: 'OEM strings',
    13: 'bios language',
    15: 'system event log',
    16: 'physical memory array',
    17: 'memory device',
    19: 'memory array mapped address',
    24: 'hardware security',
    25: 'system power controls',
    27: 'cooling device',
    32: 'system boot',
    41: 'onboard device',
    }

class DMIDecodeMonitorSource(SampleMonitorSource):
    _cmd = "dmidecode"
    
    def _get_output(self, cmd):
        import subprocess
        output = subprocess.check_output(cmd, shell=True)
        return output.decode()
    
    def _dmidecode(self, t=None):
        cmd = self._cmd
        if type != None:
            cmd = cmd + " -t " + str(t)
        
        output = self._get_output(cmd)
        return self._parse_dmi(output)
    
    def _get(self, name, results):
        return [v for j, v in results if j == name]
    
    def _parse_dmi(self, content):
        info = []
        lines = iter(content.strip().splitlines())
        while True:
            try:
                line = lines.__next__()
            except StopIteration:
                break
    
            if line.startswith('Handle 0x'):
                typ = int(line.split(',', 2)[1].strip()[len('DMI type'):])
                if typ in TYPE:
                    info.append((TYPE[typ], self._parse_handle_section(lines)))
        return info
    
    
    def _parse_handle_section(self, lines):
        data = {
            '_title': lines.__next__().rstrip(),
            }
        
        kk = None
        for line in lines:
            line = line.rstrip()
            if line.startswith('\t\t'):
                if kk != None:
                    data[kk].append(line.lstrip())
            elif line.startswith('\t'):
                k, v = [i.strip() for i in line.lstrip().split(':', 1)]
                kk = k
                if v:
                    data[k] = v
                else:
                    data[k] = []
            else:
                break
    
        return data


class BiosMonitorSource(DMIDecodeMonitorSource):
    def sample(self, parms):
        results = self._dmidecode(0)
        bios = self._get("bios", results)
        b = bios[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("Version", b["Version"])
        metricValue.addMetricValue("_title", b["_title"])
        metricValue.addMetricValue("ROM_Size", b["ROM Size"])
        metricValue.addMetricValue("BIOS_Revision", b["BIOS Revision"])
        metricValue.addMetricValue("Release_Date", b["Release Date"])
        return metricValue
        

def bios(monitorSourceName):
    monitorSource = BiosMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class SystemMonitorSource(DMIDecodeMonitorSource):
    def sample(self, parms):
        results = self._dmidecode(1)
        system = self._get("system", results)
        s = system[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("UUID", s["UUID"])
        metricValue.addMetricValue("Product_Name", s["Product Name"])
        metricValue.addMetricValue("Wakeup_Type", s["Wake-up Type"])
        metricValue.addMetricValue("Serial_Number", s["Serial Number"])
        metricValue.addMetricValue("Version", s["Version"])
        metricValue.addMetricValue("_title", s["_title"])
        metricValue.addMetricValue("Manufacturer", s["Manufacturer"])
        return metricValue

def system(monitorSourceName):
    monitorSource = SystemMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class BoardMonitorSource(DMIDecodeMonitorSource):
    def sample(self, parms):
        results = self._dmidecode(2)
        board = self._get("base board", results)
        b = board[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("Type", b["Type"])
        metricValue.addMetricValue("Asset_Tag", b["Asset Tag"])
        metricValue.addMetricValue("Version", b["Version"])
        metricValue.addMetricValue("Serial_Number", b["Serial Number"])
        metricValue.addMetricValue("Contained_Object_Handles", b["Contained Object Handles"])
        metricValue.addMetricValue("Location_In_Chassis", b["Location In Chassis"])
        metricValue.addMetricValue("Chassis_Handle", b["Chassis Handle"])
        metricValue.addMetricValue("_title", b["_title"])
        metricValue.addMetricValue("Product_Name", b["Product Name"])
        metricValue.addMetricValue("Manufacturer", b["Manufacturer"])
        return metricValue

def board(monitorSourceName):
    monitorSource = BoardMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ProcessorMonitorSource(DMIDecodeMonitorSource):
    def sample(self, parms):
        results = self._dmidecode(4)
        processor = self._get("processor", results)
        p = processor[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("Type", p["Type"])
        metricValue.addMetricValue("ID", p["ID"])
        metricValue.addMetricValue("L2_Cache_Handle", p["L2 Cache Handle"])
        metricValue.addMetricValue("Socket_Designation", p["Socket Designation"])
        metricValue.addMetricValue("_title", p["_title"])
        metricValue.addMetricValue("Core_Enabled", p["Core Enabled"])
        metricValue.addMetricValue("Asset_Tag", p["Asset Tag"])
        metricValue.addMetricValue("Max_Speed", p["Max Speed"])
        metricValue.addMetricValue("Serial_Number", p["Type"])
        metricValue.addMetricValue("Manufacturer", p["Type"])
        metricValue.addMetricValue("Thread_Count", p["Type"])
        metricValue.addMetricValue("Current_Speed", p["Type"])
        metricValue.addMetricValue("Family", p["Family"])
        metricValue.addMetricValue("External_Clock", p["External Clock"])
        metricValue.addMetricValue("L3_Cache_Handle", p["L3 Cache Handle"])
        metricValue.addMetricValue("L1_Cache_Handle", p["L1 Cache Handle"])
        metricValue.addMetricValue("Version", p["Version"])
        metricValue.addMetricValue("Status", p["Status"])
        metricValue.addMetricValue("Voltage", p["Voltage"])
        metricValue.addMetricValue("Core_Count", p["Core Count"])
        metricValue.addMetricValue("Upgrade", p["Upgrade"])
        metricValue.addMetricValue("Part_Number", p["Part Number"])
        return metricValue

def processor(monitorSourceName):
    monitorSource = ProcessorMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

if __name__ == '__main__':
    bios = ProcessorMonitorSource()
    bios.sample(None)
