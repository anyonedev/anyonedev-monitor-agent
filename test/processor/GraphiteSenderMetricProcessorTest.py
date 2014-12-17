'''
Create On 2014-12-15
注意：这不是一个单元测试，需要结合graphite服务器配合测试
@author liangzonghua
'''
import unittest
from core.MetricValue import SingleMetricValue, MultiMetricValue,\
    BatchMultiMetricValue,KeyedMultiMetricValue
from monitor.processor.GraphiteSenderMetricProcessor import GraphiteSenderMetricProcessor

class GraphiteSenderMetricProcessorTest(unittest.TestCase):
    
    processor = None
    def setUp(self):
        self.processor = GraphiteSenderMetricProcessor()
        self.processor.start()
        
    def tearDown(self):
        pass
        #if self.processor != None:
            #self.processor.stop()
            
    def test_SingleMetricValue(self):
        metricValue = SingleMetricValue("cpu_count", "count", 4)
        self.processor.process(metricValue)
    
    def test_MultiMetricValue(self):
        metricValue = MultiMetricValue("cpu")
        metricValue.addMetricValue("user2", 0.88)
        metricValue.addMetricValue("sys2", 0.23)
        self.processor.process(metricValue)
    
    def test_BatchMultiMetricVaue(self):
        batchMultiMetricValue = BatchMultiMetricValue("disk")
        metricValue = MultiMetricValue("disk")
        metricValue.addMetricValue("use", 10000)
        batchMultiMetricValue.addMetricValue(metricValue)
        metricValue = MultiMetricValue("disk")
        metricValue.addMetricValue("use", 10000)
        batchMultiMetricValue.addMetricValue(metricValue)
        self.processor.process(batchMultiMetricValue)
    
    def test_KeyedMultiMetricValue(self):
        keyedMultiMetricValue = KeyedMultiMetricValue("disk2")
        metricValue = MultiMetricValue("disk2")
        metricValue.addMetricValue("use1", 10000)
        metricValue.addMetricValue("use2", 10000)
        keyedMultiMetricValue.addMetricValue("key1",metricValue)
        metricValue = MultiMetricValue("disk2")
        metricValue.addMetricValue("use1", 10000)
        metricValue.addMetricValue("use2", 10000)
        keyedMultiMetricValue.addMetricValue("key2",metricValue)
        self.processor.process(keyedMultiMetricValue)

if __name__ == "__main__":
    unittest.main()
