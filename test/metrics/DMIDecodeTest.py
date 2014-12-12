

import unittest
from monitor.metrics.DMIDecode import bios,system, chassis,cache, portConnector,\
    systemSlot, onBoardDevice, oemString, systemConfigurationOptions,\
    physicalMemoryArray, memoryDevice, memoryError32Bit,\
    memoryArrayMappedAddress, memoryDeviceMappedAddress, voltageProbe,\
    coolingDevice, temperatureProbe, electricalCurrentProbe, systemBoot,\
    managementDevice, managementDeviceComponent, systemPowerSupply,\
    DMIDecodeMonitorSource
from core.MetricValue import MultiMetricValue,BatchMultiMetricValue
from metrics.DMIDecode import board, processor, onboardDevice

#设置dmidecode命令
DMIDecodeMonitorSource._cmd = "E:/anyonedev/dmidecode/dmidecode.exe"
class BiosMonitorSourceTest(unittest.TestCase):
    def test(self):
        monitorSource = bios("bios")
        metricValue = monitorSource.sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["Version","_title","ROM_Size","BIOS_Revision","Release_Date"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "bios监控源没有包含指标值["+metric+"]")
            
class SystemMonitorSourceTest(unittest.TestCase):
    def test(self):
        monitorSource = system("system")
        metricValue = monitorSource.sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["Version","_title","UUID","Product_Name","Wakeup_Type","Serial_Number",
                   "Manufacturer"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "system监控源没有包含指标值["+metric+"]")

class BoardMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = board("board").sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["Version","_title","Type","Asset_Tag","Serial_Number","Contained_Object_Handles",
                   "Location_In_Chassis","Chassis_Handle","Product_Name","Manufacturer"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "board监控源没有包含指标值["+metric+"]")


class ChassisMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = chassis("chassis").sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["_title","Type","Lock","Version","Serial_Number","Asset_Tag",
                   "Boot-up_State","Power_Supply_State","Thermal_State","Security_State",
                   "OEM_Infomation","Height","Number_Of_Power_Cords","Contained_Elements"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "chassis监控源没有包含指标值["+metric+"]")

class ProcessorMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = processor("processor").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["Type","_title","ID","L2_Cache_Handle","Socket_Designation","Core_Enabled",
                   "Asset_Tag","Max_Speed","Serial_Number","Manufacturer","Thread_Count",
                   "Current_Speed","Family","External_Clock","L3_Cache_Handle","L1_Cache_Handle",
                   "Version","Status","Voltage","Core_Count","Upgrade","Part_Number"]
        #print(len(metricValue.getValues()))
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                #print(value)
                self.assertNotEqual(value, None, "processor监控源没有包含指标值["+metric+"]")
           
class CacheMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = cache("cache").sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["_title","Socket_Designation","Configuration","Operational_Mode",
                   "Location","Installed_Size","Maximum_Size","Installed_SRAM_Type",
                   "Speed","Error_Correction_Type","System_Type","Associativity"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "cache监控源没有包含指标值["+metric+"]")
class PortConnectorMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = portConnector("portConnector").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Internal_Reference_Designator","Internal_Connector_Type",
                   "External_Reference_Designator","External_Connector_Type","Port_Type"]
        #print(len(metricValue.getValues()))
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                #print(value)
                self.assertNotEqual(value, None, "portConnector监控源没有包含指标值["+metric+"]")    
                
class SystemSlotMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = systemSlot("systemSlot").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Designation","Type","Current_Usage",
                   "Length","ID","Bus_Address"]
        #print(len(metricValue.getValues()))
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                #print(value)
                self.assertNotEqual(value, None, "systemSlot监控源没有包含指标值["+metric+"]")                                          

class OnBoardDeviceMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = onBoardDevice("onBoardDevice").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Type","Status","Description"]
        #print(len(metricValue.getValues()))
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                #print(value)
                self.assertNotEqual(value, None, "onboardDevice监控源没有包含指标值["+metric+"]")                                          

class OEMStringMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = oemString("OEMString").sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["_title","String_1"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "OEMString监控源没有包含指标值["+metric+"]")  
                                       
class SystemConfigurationOptionsMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = systemConfigurationOptions("systemConfigurationOptions").sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["_title","Option_1"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "systemConfigurationOptions监控源没有包含指标值["+metric+"]") 
'''
class BIOSLanguageMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = biosLanguage("biosLanguage").sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["_title","Installable_Languages","Current_Installed_Language"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "BIOSLanguage监控源没有包含指标值["+metric+"]") 
'''

class PhysicalMemoryArrayMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = physicalMemoryArray("physicalMemoryArray").sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["_title","Location","Use","Error_Correction_Type","Maximum_Capacity","Error_Information_Handle","Number_Of_Devices"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "physicalMemoryArray监控源没有包含指标值["+metric+"]") 

class MemoryDeviceMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = memoryDevice("memoryDevice").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Array_Handle","Error_Information_Handle","Total_Width",
                   "Data_Width","Size","Form_Factor","Set","Locator","Bank_Locator",
                   "Type","Type_Detail","Manufacturer","Speed","Serial_Number","Rank",
                   "Asset_Tag","Part_Number"]
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                self.assertNotEqual(value, None, "memoryDevice监控源没有包含指标值["+metric+"]")                                          

class MemoryError32BitMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = memoryError32Bit("memoryError32Bit").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Type","Granularity","Operation",
                   "Vendor_Syndrome","Memory_Array_Address","Device_Address",
                   "Resolution"]
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                self.assertNotEqual(value, None, "memoryError32Bit监控源没有包含指标值["+metric+"]")                                          

class MemoryArrayMappedAddressMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = memoryArrayMappedAddress("memoryArrayMappedAddress").sample(None)
        self.assertTrue(isinstance(metricValue,MultiMetricValue), "采样类型不对")
        metrics = ["_title","Starting_Address","Ending_Address","Range_Size",
                   "Physical_Array_Handle","Partition_Width"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "memoryArrayMappedAddress监控源没有包含指标值["+metric+"]")                                          

class MemoryDeviceMappedAddressMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = memoryDeviceMappedAddress("memoryDeviceMappedAddress").sample(None)
        self.assertTrue(isinstance(metricValue,MultiMetricValue), "采样类型不对")
        metrics = ["_title","Starting_Address","Ending_Address","Range_Size",
                   "Physical_Device_Handle","Partition_Row_Position","Memory_Array_Mapped_Address_Handle"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "memoryDeviceMappedAddress监控源没有包含指标值["+metric+"]")                                          

class VoltageProbeMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = voltageProbe("voltageProbe").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Description","Location","Status",
                   "Maximum_Value","Minimum_Value","Resolution",
                   "Tolerance","Accuracy","OEM-specific_Information","Nominal_Value"]
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                self.assertNotEqual(value, None, "voltageProbe监控源没有包含指标值["+metric+"]")                                          

class CoolingDeviceMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = coolingDevice("coolingDevice").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Temperatur_Probe_Handle","Type","Status",
                   "Cooling_Unit_Group","OEM-specific_Information","Nominal_Speed"]
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                self.assertNotEqual(value, None, "coolingDevice监控源没有包含指标值["+metric+"]")                                          

class TemperatureProbeMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = temperatureProbe("temperatureProbe").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Description","Location","Status",
                   "Maximum_Value","Minimum_Value","Resolution",
                   "Tolerance","Accuracy","OEM-specific_Information","Nominal_Value"]
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                self.assertNotEqual(value, None, "temperatureProbe监控源没有包含指标值["+metric+"]")                                          

class ElectricalCurrentProbeMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = electricalCurrentProbe("electricalCurrentProbe").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Description","Location","Status",
                   "Maximum_Value","Minimum_Value","Resolution",
                   "Tolerance","Accuracy","OEM-specific_Information","Nominal_Value"]
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                self.assertNotEqual(value, None, "electricalCurrentProbe监控源没有包含指标值["+metric+"]")                                          

class SystemBootMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = systemBoot("systemBoot").sample(None)
        self.assertTrue(isinstance(metricValue,MultiMetricValue), "采样类型不对")
        metrics = ["_title","Status"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "systemBoot监控源没有包含指标值["+metric+"]")                                          

class ManagementDeviceMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = managementDevice("managementDevice").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Description","Type","Address","Address_Type"]
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                self.assertNotEqual(value, None, "managementDevice监控源没有包含指标值["+metric+"]")                                          

class ManagementDeviceComponentMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = managementDeviceComponent("managementDeviceComponent").sample(None)
        self.assertTrue(isinstance(metricValue, BatchMultiMetricValue), "采样类型不对")
        metrics = ["_title","Description","Management_Device_Handle","Component_Handle","Threshold_Handle"]
        for values in metricValue.getValues():
            for metric in metrics:
                value = values.getValue(metric)
                self.assertNotEqual(value, None, "managementDeviceComponent监控源没有包含指标值["+metric+"]")                                          

class SystemPowerSupplyMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = systemPowerSupply("systemPowerSupply").sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["_title","Power_Unit_Group","Location","Name",
                   "Manufacturer","Serial_Number","Asset_Tag","Model_Part_Number","Revision",
                   "Max_Power_Capacity","Status","Type","Input_Voltage_Range_Switching",
                   "Plugged","Hot_Replaceable","Input_Voltage_Probe_Handle",
                   "Cooling_Device_Handle","Input_Current_Probe_Handle"]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "systemPowerSupply监控源没有包含指标值["+metric+"]")                                          

class OnboardDeviceMonitorSourceTest(unittest.TestCase):
    def test(self):
        metricValue = onboardDevice("onboardDevice").sample(None)
        self.assertTrue(isinstance(metricValue, MultiMetricValue), "采样类型不对")
        metrics = ["_title","Type","Status","Type_Instance",
                   "Bus_Address","Reference_Designation",]
        for metric in metrics:
            value = metricValue.getValue(metric)
            self.assertNotEqual(value, None, "onboardDevice监控源没有包含指标值["+metric+"]")                                          

if __name__ == "__main__":
    unittest.main()           