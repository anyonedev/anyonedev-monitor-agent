from processor.ChainMetricProcessor import ChainMetricProcessor
from processor.InfluxDBSenderMetricProcessor import InfluxDBSenderMetricProcessor
from processor.LoggingMetricProcessor import LoggingMetricProcessor
from processor.ScheduleMetricProcessor import ScheduleMetricProcessor


def influxDBSender():
    pass

def chain(*args):
    p = ChainMetricProcessor()
    for arg in args:
        p.processor(arg)
    
    return p

def logging():
    return LoggingMetricProcessor()

def interval_schedule(interval=1, monitorSourceMatcher=None, processor=None):
    p = ScheduleMetricProcessor()
    p.interval(interval, monitorSourceMatcher, processor)
    return p
    

def influxdb_sender():
    return InfluxDBSenderMetricProcessor()
