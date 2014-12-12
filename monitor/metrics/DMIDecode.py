'''
使用DMIDecode采集硬件信息
@author: wushiqi,liangzonghua
Create On 2014-12-1
'''
from core import regist_monitor_source
from core.MetricValue import MultiMetricValue,BatchMultiMetricValue
from core.MonitorSource import SampleMonitorSource


TYPE = {
    0:  'bios',
    1:  'system',
    2:  'base board',
    3:  'Chassis',
    4:  'processor',
    7:  'cache',
    8:  'port connector',
    9:  'system slot',
    10: 'on board device',
    11: 'OEM strings',
    12: 'System Configuration Options',
    13: 'bios language',
    16: 'physical memory array',
    17: 'memory device',
    18: '32-bit Memory Error',
    19: 'memory array mapped address',
    20: 'Memory Device Mapped Address',
    26: 'Voltage Probe',
    27: 'cooling device',
    28: 'Temperature Probe',
    29: 'Electrical Current Probe',
    32: 'system boot',
    34: 'Management Device',
    35: 'Management Device Component',
    39: 'Power Supply',
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
    dmidecode = 0
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        bios = self._get(TYPE[self.dmidecode], results)
        b = bios[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("Version", b["Version"])
        metricValue.addMetricValue("_title", b["_title"])
        metricValue.addMetricValue("ROM_Size", b["ROM Size"])
        metricValue.addMetricValue("BIOS_Revision", b["BIOS Revision"])
        metricValue.addMetricValue("Release_Date", b["Release Date"])
        return metricValue
    
def bios(monitorSourceName=TYPE[BiosMonitorSource.dmidecode]):
    monitorSource = BiosMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class SystemMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 1
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        system = self._get(TYPE[self.dmidecode], results)
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

def system(monitorSourceName=TYPE[SystemMonitorSource.dmidecode]):
    monitorSource = SystemMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class BoardMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 2
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        board = self._get(TYPE[self.dmidecode], results)
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

class ChassisMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 3
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        chassis = self._get(TYPE[self.dmidecode], results)
        c = chassis[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", c["_title"])
        metricValue.addMetricValue("Manufacturer",c["Manufacturer"])
        metricValue.addMetricValue("Type",c["Type"])
        metricValue.addMetricValue("Lock",c["Lock"])
        metricValue.addMetricValue("Version",c["Version"])
        metricValue.addMetricValue("Serial_Number",c["Serial Number"])
        metricValue.addMetricValue("Asset_Tag",c["Asset Tag"])
        metricValue.addMetricValue("Boot-up_State",c["Boot-up State"])
        metricValue.addMetricValue("Power_Supply_State",c["Power Supply State"])
        metricValue.addMetricValue("Thermal_State",c["Thermal State"])
        metricValue.addMetricValue("Security_State",c["Security Status"])
        metricValue.addMetricValue("OEM_Infomation",c["OEM Information"])
        metricValue.addMetricValue("Height",c["Height"])
        metricValue.addMetricValue("Number_Of_Power_Cords",c["Number Of Power Cords"])
        metricValue.addMetricValue("Contained_Elements",c["Contained Elements"])
        return metricValue

def chassis(monitorSourceName=TYPE[ChassisMonitorSource.dmidecode]):
    monitorSource = ChassisMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ProcessorMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 4
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        processor = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for p in processor:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("Type", p["Type"])
            metricValue.addMetricValue("ID", p["ID"])
            metricValue.addMetricValue("L2_Cache_Handle", p["L2 Cache Handle"])
            metricValue.addMetricValue("Socket_Designation", p["Socket Designation"])
            metricValue.addMetricValue("_title", p["_title"])
            metricValue.addMetricValue("Core_Enabled", p["Core Enabled"])
            metricValue.addMetricValue("Asset_Tag", p["Asset Tag"])
            metricValue.addMetricValue("Max_Speed", p["Max Speed"])
            metricValue.addMetricValue("Serial_Number", p["Serial Number"])
            metricValue.addMetricValue("Manufacturer", p["Manufacturer"])
            metricValue.addMetricValue("Thread_Count", p["Thread Count"])
            metricValue.addMetricValue("Current_Speed", p["Current Speed"])
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
            
            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue

def processor(monitorSourceName=TYPE[ProcessorMonitorSource.dmidecode]):
    monitorSource = ProcessorMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class CacheMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 7
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        cache = self._get(TYPE[self.dmidecode], results)
        c = cache[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", c["_title"])
        metricValue.addMetricValue("Socket_Designation", c["Socket Designation"])
        metricValue.addMetricValue("Configuration", c["Configuration"])
        metricValue.addMetricValue("Operational_Mode", c["Operational Mode"])
        metricValue.addMetricValue("Location", c["Location"])
        metricValue.addMetricValue("Installed_Size", c["Installed Size"])
        metricValue.addMetricValue("Maximum_Size", c["Maximum Size"])
        metricValue.addMetricValue("Installed_SRAM_Type", c["Installed SRAM Type"])
        metricValue.addMetricValue("Speed", c["Speed"])
        metricValue.addMetricValue("Error_Correction_Type", c["Error Correction Type"])
        metricValue.addMetricValue("System_Type", c["System Type"])
        metricValue.addMetricValue("Associativity", c["Associativity"])
        return metricValue
        
def cache(monitorSourceName=TYPE[CacheMonitorSource.dmidecode]):  
    monitorSource = CacheMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource
        
        
class PortConnectorMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 8
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        portConnector = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in portConnector:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Internal_Reference_Designator", item["Internal Reference Designator"])
            metricValue.addMetricValue("Internal_Connector_Type", item["Internal Connector Type"])
            metricValue.addMetricValue("External_Reference_Designator", item["External Reference Designator"])
            metricValue.addMetricValue("External_Connector_Type", item["External Connector Type"])
            metricValue.addMetricValue("Port_Type", item["Port Type"])
            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def portConnector(monitorSourceName=TYPE[PortConnectorMonitorSource.dmidecode]):  
    monitorSource = PortConnectorMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource        

class SystemSlotMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 9
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        systemSlot = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in systemSlot:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Designation", item["Designation"])
            metricValue.addMetricValue("Type", item["Type"])
            metricValue.addMetricValue("Current_Usage", item["Current Usage"])
            metricValue.addMetricValue("Length", item["Length"])
            metricValue.addMetricValue("ID", item["ID"])
            metricValue.addMetricValue("Bus_Address", item["Bus Address"])
            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def systemSlot(monitorSourceName=TYPE[SystemMonitorSource.dmidecode]):  
    monitorSource = SystemSlotMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource       

class OnBoardDeviceMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 10
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        systemSlot = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in systemSlot:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Type", item["Type"])
            metricValue.addMetricValue("Status", item["Status"])
            metricValue.addMetricValue("Description", item["Description"])
            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def onBoardDevice(monitorSourceName=TYPE[SystemMonitorSource.dmidecode]):  
    monitorSource = OnBoardDeviceMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource 
        
        
class OEMStringMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 11
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        OEMString = self._get(TYPE[self.dmidecode], results)
        item = OEMString[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", item["_title"])
        metricValue.addMetricValue("String_1", item["String 1"])
        return metricValue
        
def oemString(monitorSourceName=TYPE[OEMStringMonitorSource.dmidecode]):  
    monitorSource = OEMStringMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource  

class SystemConfigurationOptionsMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 12
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        item = items[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", item["_title"])
        metricValue.addMetricValue("Option_1", item["Option 1"])
        return metricValue
        
def systemConfigurationOptions(monitorSourceName=TYPE[SystemConfigurationOptionsMonitorSource.dmidecode]):  
    monitorSource = SystemConfigurationOptionsMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource 
'''
class BIOSLanguageMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 13
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        item = items[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", item["_title"])
        metricValue.addMetricValue("Installable_Languages", item["Installable Languages"])
        metricValue.addMetricValue("Current_Installed_Language", item["Current Installed Language"])
        return metricValue
        
def biosLanguage(monitorSourceName=TYPE[SystemConfigurationOptionsMonitorSource.dmidecode]):  
    monitorSource = BIOSLanguageMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource  
'''

class PhysicalMemoryArrayMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 16
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        item = items[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", item["_title"])
        metricValue.addMetricValue("Location", item["Location"])
        metricValue.addMetricValue("Use", item["Use"])
        metricValue.addMetricValue("Error_Correction_Type", item["Error Correction Type"])
        metricValue.addMetricValue("Maximum_Capacity", item["Maximum Capacity"])
        metricValue.addMetricValue("Error_Information_Handle", item["Error Information Handle"])
        metricValue.addMetricValue("Number_Of_Devices", item["Number Of Devices"])
        return metricValue
        
def physicalMemoryArray(monitorSourceName=TYPE[PhysicalMemoryArrayMonitorSource.dmidecode]):  
    monitorSource = PhysicalMemoryArrayMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource


class MemoryDeviceMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 17
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in items:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Array_Handle", item["Array Handle"])
            metricValue.addMetricValue("Error_Information_Handle", item["Error Information Handle"])
            metricValue.addMetricValue("Total_Width", item["Total Width"])
            metricValue.addMetricValue("Data_Width", item["Data Width"])
            metricValue.addMetricValue("Size", item["Size"])
            metricValue.addMetricValue("Form_Factor", item["Form Factor"])
            metricValue.addMetricValue("Set", item["Set"])
            metricValue.addMetricValue("Locator", item["Locator"])
            metricValue.addMetricValue("Bank_Locator", item["Bank Locator"])
            metricValue.addMetricValue("Type", item["Type"])
            metricValue.addMetricValue("Type_Detail", item["Type Detail"])
            metricValue.addMetricValue("Manufacturer", item["Manufacturer"])
            metricValue.addMetricValue("Speed", item["Speed"])
            metricValue.addMetricValue("Serial_Number", item["Serial Number"])
            metricValue.addMetricValue("Rank", item["Rank"])
            metricValue.addMetricValue("Asset_Tag", item["Asset Tag"])
            metricValue.addMetricValue("Part_Number", item["Part Number"])
            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def memoryDevice(monitorSourceName=TYPE[MemoryDeviceMonitorSource.dmidecode]):  
    monitorSource = MemoryDeviceMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource  

class MemoryError32BitMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 18
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in items:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Type", item["Type"])
            metricValue.addMetricValue("Granularity", item["Granularity"])
            metricValue.addMetricValue("Operation", item["Operation"])
            metricValue.addMetricValue("Vendor_Syndrome", item["Vendor Syndrome"])
            metricValue.addMetricValue("Memory_Array_Address", item["Memory Array Address"])
            metricValue.addMetricValue("Device_Address", item["Device Address"])
            metricValue.addMetricValue("Resolution", item["Resolution"])

            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def memoryError32Bit(monitorSourceName=TYPE[MemoryError32BitMonitorSource.dmidecode]):  
    monitorSource = MemoryError32BitMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource
        
class MemoryArrayMappedAddressMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 19
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        item = items[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", item["_title"])
        metricValue.addMetricValue("Starting_Address", item["Starting Address"])
        metricValue.addMetricValue("Ending_Address", item["Ending Address"])
        metricValue.addMetricValue("Range_Size", item["Range Size"])
        metricValue.addMetricValue("Physical_Array_Handle", item["Physical Array Handle"])
        metricValue.addMetricValue("Partition_Width", item["Partition Width"])
        return metricValue
        
def memoryArrayMappedAddress(monitorSourceName=TYPE[MemoryArrayMappedAddressMonitorSource.dmidecode]):  
    monitorSource = MemoryArrayMappedAddressMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource  

class MemoryDiviceMappedAddressMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 20
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        item = items[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", item["_title"])
        metricValue.addMetricValue("Starting_Address", item["Starting Address"])
        metricValue.addMetricValue("Ending_Address", item["Ending Address"])
        metricValue.addMetricValue("Range_Size", item["Range Size"])
        metricValue.addMetricValue("Physical_Device_Handle", item["Physical Device Handle"])
        metricValue.addMetricValue("Partition_Row_Position", item["Partition Row Position"])
        metricValue.addMetricValue("Memory_Array_Mapped_Address_Handle", item["Memory Array Mapped Address Handle"])
        return metricValue
        
def memoryDeviceMappedAddress(monitorSourceName=TYPE[MemoryDiviceMappedAddressMonitorSource.dmidecode]):  
    monitorSource = MemoryDiviceMappedAddressMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource  

class VoltageProbeMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 26
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in items:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Description", item["Description"])
            metricValue.addMetricValue("Location", item["Location"])
            metricValue.addMetricValue("Status", item["Status"])
            metricValue.addMetricValue("Maximum_Value", item["Maximum Value"])
            metricValue.addMetricValue("Minimum_Value", item["Minimum Value"])
            metricValue.addMetricValue("Resolution", item["Resolution"])
            metricValue.addMetricValue("Tolerance", item["Tolerance"])
            metricValue.addMetricValue("Accuracy", item["Accuracy"])
            metricValue.addMetricValue("OEM-specific_Information", item["OEM-specific Information"])
            metricValue.addMetricValue("Nominal_Value", item["Nominal Value"])

            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def voltageProbe(monitorSourceName=TYPE[VoltageProbeMonitorSource.dmidecode]):  
    monitorSource = VoltageProbeMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class CoolingDeviceMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 27
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in items:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Temperatur_Probe_Handle", item["Temperature Probe Handle"])
            metricValue.addMetricValue("Type", item["Type"])
            metricValue.addMetricValue("Status", item["Status"])
            metricValue.addMetricValue("Cooling_Unit_Group", item["Cooling Unit Group"])
            metricValue.addMetricValue("OEM-specific_Information", item["OEM-specific Information"])
            metricValue.addMetricValue("Nominal_Speed", item["Nominal Speed"])

            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def coolingDevice(monitorSourceName=TYPE[CoolingDeviceMonitorSource.dmidecode]):  
    monitorSource = CoolingDeviceMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class TemperatureProbeMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 28
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in items:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Description", item["Description"])
            metricValue.addMetricValue("Location", item["Location"])
            metricValue.addMetricValue("Status", item["Status"])
            metricValue.addMetricValue("Maximum_Value", item["Maximum Value"])
            metricValue.addMetricValue("Minimum_Value", item["Minimum Value"])
            metricValue.addMetricValue("Resolution", item["Resolution"])
            metricValue.addMetricValue("Tolerance", item["Tolerance"])
            metricValue.addMetricValue("Accuracy", item["Accuracy"])
            metricValue.addMetricValue("OEM-specific_Information", item["OEM-specific Information"])
            metricValue.addMetricValue("Nominal_Value", item["Nominal Value"])

            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def temperatureProbe(monitorSourceName=TYPE[TemperatureProbeMonitorSource.dmidecode]):  
    monitorSource = TemperatureProbeMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ElectricalCurrentProbeMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 29
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in items:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Description", item["Description"])
            metricValue.addMetricValue("Location", item["Location"])
            metricValue.addMetricValue("Status", item["Status"])
            metricValue.addMetricValue("Maximum_Value", item["Maximum Value"])
            metricValue.addMetricValue("Minimum_Value", item["Minimum Value"])
            metricValue.addMetricValue("Resolution", item["Resolution"])
            metricValue.addMetricValue("Tolerance", item["Tolerance"])
            metricValue.addMetricValue("Accuracy", item["Accuracy"])
            metricValue.addMetricValue("OEM-specific_Information", item["OEM-specific Information"])
            metricValue.addMetricValue("Nominal_Value", item["Nominal Value"])

            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def electricalCurrentProbe(monitorSourceName=TYPE[ElectricalCurrentProbeMonitorSource.dmidecode]):  
    monitorSource = ElectricalCurrentProbeMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class SystemBootMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 32
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        item = items[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", item["_title"])
        metricValue.addMetricValue("Status", item["Status"])
        return metricValue
        
def systemBoot(monitorSourceName=TYPE[SystemBootMonitorSource.dmidecode]):  
    monitorSource = SystemBootMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ManagementDeviceMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 34
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in items:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Description", item["Description"])
            metricValue.addMetricValue("Type", item["Type"])
            metricValue.addMetricValue("Address", item["Address"])
            metricValue.addMetricValue("Address_Type", item["Address Type"])

            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def managementDevice(monitorSourceName=TYPE[ManagementDeviceMonitorSource.dmidecode]):  
    monitorSource = ManagementDeviceMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class ManagementDeviceComponentMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 35
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        batchMetricValue = BatchMultiMetricValue(self.getMonitorSourceName())
        for item in items:
            metricValue = MultiMetricValue(self.getMonitorSourceName())
            metricValue.addMetricValue("_title", item["_title"])
            metricValue.addMetricValue("Description", item["Description"])
            metricValue.addMetricValue("Management_Device_Handle", item["Management Device Handle"])
            metricValue.addMetricValue("Component_Handle", item["Component Handle"])
            metricValue.addMetricValue("Threshold_Handle", item["Threshold Handle"])

            batchMetricValue.addMetricValue(metricValue)
        return batchMetricValue
        
def managementDeviceComponent(monitorSourceName=TYPE[ManagementDeviceComponentMonitorSource.dmidecode]):  
    monitorSource = ManagementDeviceComponentMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource


class SystemPowerSupplyMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 39
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        item = items[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", item["_title"])
        metricValue.addMetricValue("Power_Unit_Group", item["Power Unit Group"])
        metricValue.addMetricValue("Location", item["Location"])
        metricValue.addMetricValue("Name", item["Name"])
        metricValue.addMetricValue("Manufacturer", item["Manufacturer"])
        metricValue.addMetricValue("Serial_Number", item["Serial Number"])
        metricValue.addMetricValue("Asset_Tag", item["Asset Tag"])
        metricValue.addMetricValue("Model_Part_Number", item["Model Part Number"])
        metricValue.addMetricValue("Revision", item["Revision"])
        metricValue.addMetricValue("Max_Power_Capacity", item["Max Power Capacity"])
        metricValue.addMetricValue("Status", item["Status"])
        metricValue.addMetricValue("Type", item["Type"])
        metricValue.addMetricValue("Input_Voltage_Range_Switching", item["Input Voltage Range Switching"])
        metricValue.addMetricValue("Plugged", item["Plugged"])
        metricValue.addMetricValue("Hot_Replaceable", item["Hot Replaceable"])
        metricValue.addMetricValue("Input_Voltage_Probe_Handle", item["Input Voltage Probe Handle"])
        metricValue.addMetricValue("Cooling_Device_Handle", item["Cooling Device Handle"])
        metricValue.addMetricValue("Input_Current_Probe_Handle", item["Input Current Probe Handle"])
        return metricValue
        
def systemPowerSupply(monitorSourceName=TYPE[SystemPowerSupplyMonitorSource.dmidecode]):  
    monitorSource = SystemPowerSupplyMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

class OnboardDeviceMonitorSource(DMIDecodeMonitorSource):
    dmidecode = 41
    def sample(self, parms):
        results = self._dmidecode(self.dmidecode)
        items = self._get(TYPE[self.dmidecode], results)
        item = items[0]
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("_title", item["_title"])
        metricValue.addMetricValue("Type", item["Type"])
        metricValue.addMetricValue("Status", item["Status"])
        metricValue.addMetricValue("Type_Instance", item["Type Instance"])
        metricValue.addMetricValue("Bus_Address", item["Bus Address"])
        metricValue.addMetricValue("Reference_Designation", item["Reference Designation"])
        return metricValue
        
def onboardDevice(monitorSourceName=TYPE[OnboardDeviceMonitorSource.dmidecode]):  
    monitorSource = OnboardDeviceMonitorSource()
    monitorSource.monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource 