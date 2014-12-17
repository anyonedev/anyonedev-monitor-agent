#开发指南
本监控产品开发主要包括监控源和指标处理器开发。
### 监控源
1 添加可采样的CPUTimes监控源

```
class CpuTimesMonitorSource(SampleMonitorSource):
    def sample(self, parms):
        cpu = psutil.cpu_times()
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValue("user", cpu.user)
        metricValue.addMetricValue("system", cpu.system)
        metricValue.addMetricValue("idle", cpu.idle)
        return metricValue
```
2 注册到监控源注册表中

```
def cpu_times(monitorSourceName):
    monitorSource = CpuTimesMonitorSource().monitorSourceName(monitorSourceName)
    regist_monitor_source(monitorSource)
    return monitorSource

cpu_times("cpu_times")
```

3 注册到定时调度器中

```
cpuTimesPercentScheduler = interval_schedule(interval, monitor_source_name_matcher("cpu_times_percent"), logging)
regist_metric_processor("cpu_times_percent", cpuTimesPercentScheduler)
```

### 添加指标处理器
1 添加日志处理器
```
class LoggingMetricProcessor(MetricProcessor):

    def start(self):
        pass

    def process(self, metricValue:MetricValue):
        clientId = metricValue.getClientId()
        monitorSourceName = metricValue.getMonitorSourceName()
        sampleTime = metricValue.getSampleTime()

        if isinstance(metricValue, MultiMetricValue):
            info(metricValue.getValues())
        elif isinstance(metricValue, SingleMetricValue):
            info(metricValue.getMetricValue())


    def stop(self):
        pass

    def fail(self):
        pass
```
2 使用日志处理器
```
loggingMetricProcessor = LoggingMetricProcessor()
cpuTimesPercentScheduler = interval_schedule(interval, monitor_source_name_matcher("cpu_times_percent"), loggingMetricProcessor)
regist_metric_processor("cpu_times_percent", cpuTimesPercentScheduler)
```
