
import unittest
import time
from monitor.processor.ZeroMQSenderMetricProcessor import ZeroMQSenderMetricProcessor
import zmq
from monitor.core.MetricValue import SingleMetricValue

class ZeroMQSenderMetricProcessorTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    
    def test_singleMetricValue(self):
        try:
            self.processor = ZeroMQSenderMetricProcessor("127.0.0.1",5555,"tcp", zmq.PUB,"")
            self.processor.start()
            
            metricValue = SingleMetricValue("cpu_count","count",4)
            index = 0
            
            while index<10:
                self.processor.process(metricValue)
                print("index:"+str(index))
                time.sleep(1)
                index = index+1
        except Exception as ex:
            print(ex)
            self.fail("single metricValue send to zeromq failure")
    
    def test_multiMetricValue(self):
        pass
    
    def test_batchMultiMetricValue(self):
        pass

    def test_keyedMultiMetricValue(self):
        pass
    
    
if __name__ == "__main__":
    unittest.main()