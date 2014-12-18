from monitor.core.MetricValue import MetricValue,SingleMetricValue,\
    KeyedMultiMetricValue, MultiMetricValue, BatchMultiMetricValue
import json

def toJSON(metricValue:MetricValue):
        if metricValue == None:
            return "{}"
        rs = dict()
        rs["clientId"] = metricValue.getClientId()
        rs["sampleTime"] = metricValue.getSampleTime()
        rs["monitorSourceName"] = metricValue.getMonitorSourceName()
        values = None
        if isinstance(metricValue, SingleMetricValue):
            values = dict()
            values[metricValue.getMetricName()] = metricValue.getMetricValue()
        elif isinstance(metricValue, MultiMetricValue):
            values = dict()
            if metricValue.getValues() != None:
                for key,value in metricValue.getValues().items():
                    values[key] = value
        elif isinstance(metricValue, BatchMultiMetricValue):
            values = []
            for multiMetricValue in metricValue.getValues():
                if multiMetricValue.getValues() != None:
                    items = dict()
                    for key,value in multiMetricValue.getValues().items():
                        items[key] = value
                    values.append(items)
        elif isinstance(metricValue, KeyedMultiMetricValue):
            if metricValue.getValues() != None:
                values = dict()
                for key,multiMetricValue in metricValue.getValues().items():
                    if multiMetricValue.getValues() != None:
                        items = dict()
                        for k,v in multiMetricValue.getValues().items():
                            items[k] = v
                        values[key] = items
        else:
            print("非MetricValue类型")
        rs["values"] = values
        
        return json.dumps(rs)
        
def toMetricValue():
    pass
    
    
    
if __name__ == "__main__":
    single = SingleMetricValue("cpu_count","count",4)
    print(toJSON(single))
    multi = MultiMetricValue("cpu_count")
    multi.addMetricValue("count1", 4)
    multi.addMetricValue("count2", 2)
    multi.addMetricValue("count3", 1)
    print(toJSON(multi))
    
    batch = BatchMultiMetricValue("cpu_count")
    multi = MultiMetricValue("cpu_count")
    multi.addMetricValue("count1", 4)
    multi.addMetricValue("count2", 2)
    multi.addMetricValue("count3", 1)
    batch.addMetricValue(multi)
    multi = MultiMetricValue("cpu_count")
    multi.addMetricValue("count1", 4)
    multi.addMetricValue("count2", 2)
    multi.addMetricValue("count3", 1)
    batch.addMetricValue(multi)
    print(toJSON(batch))
    
    keyed = KeyedMultiMetricValue("cpu_count")
    multi = MultiMetricValue("cpu_count")
    multi.addMetricValue("count1", 4)
    multi.addMetricValue("count2", 2)
    multi.addMetricValue("count3", 1)
    keyed.addMetricValue("key1",multi)
    multi = MultiMetricValue("cpu_count")
    multi.addMetricValue("count1", 4)
    multi.addMetricValue("count2", 2)
    multi.addMetricValue("count3", 1)
    keyed.addMetricValue("key2",multi)
    print(toJSON(keyed))
