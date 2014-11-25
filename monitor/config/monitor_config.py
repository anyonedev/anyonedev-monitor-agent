'''
Created on 2014-11-12

@author: hongye
'''
from core import monitor_source_name_matcher
from core import regist_metric_processor
from metrics.Cpu import cpu_percent
from metrics.Cpu import cpu_times
from metrics.Cpu import cpu_times_percent
from metrics.Disk import disk_io_counters
from metrics.Disk import disk_partitions
from metrics.Disk import disk_usage
from metrics.Memory import virtual_memory, swap_memory
from metrics.Network import net_connections
from metrics.Network import net_io_counters
from metrics.Process import process_info, pid_provider, process_io_counters, \
    process_cpu_percent, process_memory_percent, process_connections, \
    process_num_threads, cmd_pid_provider
from processor import interval_schedule, HTTPExportMetricProcessor
from processor import logging, influxdb_sender, chain


virtual_memory("virtual_memory")
swap_memory("swap_memory")
cpu_percent("cpu_percent")
cpu_times("cpu_times")
cpu_times_percent("cpu_times_percent")

disk_usage("disk_usage.root", "/")
disk_io_counters("disk_io_counters", False)
disk_io_counters("disk_io_counters.perdisk", True)
disk_partitions("disk_partitions")

net_connections("net_connections.inet")
net_io_counters("net_io_counters", False)
net_io_counters("net_io_counters.pernic", True)

outworkerProcessProvider = cmd_pid_provider("jps -l | grep geronimo | awk '{print $1}'") 
# pid_provider(9032)

process_info("process.outworker", outworkerProcessProvider)
process_io_counters("process.outworker.io_counters", outworkerProcessProvider)
process_cpu_percent("process.outworker.cpu_percent", outworkerProcessProvider)
process_memory_percent("process.outworker.memory_percent", outworkerProcessProvider)
process_connections("process.outworker.connections", outworkerProcessProvider)
process_num_threads("process.outworker.num_threads", outworkerProcessProvider)

influxSender = influxdb_sender()
logging = logging()

metricProcessor = chain(logging, influxSender)

interval = 10
 
virtualMemoryScheduler = interval_schedule(interval, monitor_source_name_matcher("virtual_memory"), influxdb_sender())
regist_metric_processor("virtual_memory", virtualMemoryScheduler)
     
swapMemoryScheduler = interval_schedule(interval, monitor_source_name_matcher("swap_memory"), influxdb_sender())
regist_metric_processor("swap_memory", swapMemoryScheduler)
   
cpuPercentScheduler = interval_schedule(interval, monitor_source_name_matcher("cpu_percent"), influxdb_sender())
regist_metric_processor("cpu_percent", cpuPercentScheduler)
    
cpuTimesScheduler = interval_schedule(interval, monitor_source_name_matcher("cpu_times"), influxdb_sender())
regist_metric_processor("cpu_times", cpuTimesScheduler)
      
cpuTimesPercentScheduler = interval_schedule(interval, monitor_source_name_matcher("cpu_times_percent"), influxdb_sender())
regist_metric_processor("cpu_times_percent", cpuTimesPercentScheduler)
    
diskUsageScheduler = interval_schedule(interval, monitor_source_name_matcher("disk_usage.root"), influxdb_sender())
regist_metric_processor("disk_usage.root", diskUsageScheduler)
    
diskIoCountersScheduler = interval_schedule(interval, monitor_source_name_matcher("disk_io_counters"), influxdb_sender())
regist_metric_processor("disk_io_counters", diskIoCountersScheduler)
     
diskIoCountersPerdiskScheduler = interval_schedule(interval, monitor_source_name_matcher("disk_io_counters.perdisk"), influxdb_sender())
regist_metric_processor("disk_io_counters.perdisk", diskIoCountersPerdiskScheduler)
     
diskPartitionsScheduler = interval_schedule(interval, monitor_source_name_matcher("disk_partitions"), influxdb_sender())
regist_metric_processor("disk_partitions", diskPartitionsScheduler)
    
netConnectionsInetScheduler = interval_schedule(interval, monitor_source_name_matcher("net_connections.inet"), influxdb_sender())
regist_metric_processor("net_connections.inet", netConnectionsInetScheduler)
   
netIoCountersInetScheduler = interval_schedule(interval, monitor_source_name_matcher("net_io_counters"), influxdb_sender())
regist_metric_processor("net_io_counters", netIoCountersInetScheduler)
 
netIoCountersPernicScheduler = interval_schedule(interval, monitor_source_name_matcher("net_io_counters.pernic"), metricProcessor)
regist_metric_processor("net_io_counters.pernic", netIoCountersPernicScheduler)

# processOutworkerScheduler = interval_schedule(interval, monitor_source_name_matcher("process.outworker"), logging)
# regist_metric_processor("process.outworker", processOutworkerScheduler)

processIoCountersScheduler = interval_schedule(interval, monitor_source_name_matcher("process.outworker.io_counters"), influxdb_sender())
regist_metric_processor("process.outworker.io_counters", processIoCountersScheduler)

processCpuPercentScheduler = interval_schedule(interval, monitor_source_name_matcher("process.outworker.cpu_percent"), influxdb_sender())
regist_metric_processor("process.outworker.cpu_percent", processCpuPercentScheduler)

processMemoryPercentScheduler = interval_schedule(interval, monitor_source_name_matcher("process.outworker.memory_percent"), influxdb_sender())
regist_metric_processor("process.outworker.memory_percent", processMemoryPercentScheduler)

# processConnectionsScheduler = interval_schedule(interval, monitor_source_name_matcher("process.outworker.connections"), logging)
# regist_metric_processor("process.outworker.connections", processConnectionsScheduler)

processNumThreadsScheduler = interval_schedule(interval, monitor_source_name_matcher("process.outworker.num_threads"), influxdb_sender())
regist_metric_processor("process.outworker.num_threads", processNumThreadsScheduler)

exportHttpJson = HTTPExportMetricProcessor.http_json_export()
regist_metric_processor("export.http.json", exportHttpJson)