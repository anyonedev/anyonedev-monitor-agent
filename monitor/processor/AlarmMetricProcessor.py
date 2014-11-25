'''
Created on 2014-11-18

@author: hongye
'''

from pyformance import registry
from core.MetricProcessor import MetricProcessor


class AlarmSendStrategy(object):
    pass

class AlarmSender(object):
    _strategy = None
    
    def send(self):
        pass

class AlarmMetricProcessor(MetricProcessor):
    _alarmSender = None

class PercentlineMetricProcessor(AlarmMetricProcessor):
    pass

class CounterMetricProcessor(AlarmMetricProcessor):
    pass

class ThresholdMetricProcessor(AlarmMetricProcessor):
    pass

