# -*- coding: utf-8 -*-
import unittest
import os
import csv
import shutil
from time import time
from monitor.processor.CSVMetricProcessor import CSVMetricProcessor
from core.MetricValue import SingleMetricValue, MultiMetricValue,\
    BatchMultiMetricValue,KeyedMultiMetricValue

class CSVMetricProcessorTest(unittest.TestCase):
    #测试环境配置
    linux = dict()
    linux["workDirectory"] = "/data/csv/work/cpu"
    linux["backupDirectory"] = "/data/csv/backup/cpu"
    linux["backupInterval"] = 30*60*1000
    windows = dict()
    windows["workDirectory"] = "C:/csv/work/cpu"
    windows["backupDirectory"] = "C:/csv/backup/cpu"
    windows["backupInterval"] = 30*60*1000
    config = dict()
    config["posix"] = linux
    config["nt"]= windows
    
    __processor = None
    
    def setUp(self):
        #设置参数
        self.__config = CSVMetricProcessorTest.config[os.name]
        #清除目录
        if os.path.exists(self.__config["workDirectory"]):
            shutil.rmtree(self.__config["workDirectory"])
        
    def tearDown(self):
        #停止processor
        if self.__processor != None:
            self.__processor.stop()
    
    def test___init__(self):
        '''
                测试构造函数
        '''
        try:
            CSVMetricProcessor()
            self.fail("参数配置不齐通过")
        except:
            pass
        try:
            CSVMetricProcessor(self.__config["workDirectory"])
            self.fail("参数配置不齐通过")
        except:
            pass
        try:
            CSVMetricProcessor("",self.__config["backupDirectory"])
            self.fail("参数配置不齐通过")
        except:
            pass
        
        self.__processor = CSVMetricProcessor(self.__config["workDirectory"],self.__config["backupDirectory"])
        self.__processor.start()
        
    def testBackupFunction(self):
        '''
               测试备份策略
        '''
        processor = CSVMetricProcessor(self.__config["workDirectory"],self.__config["backupDirectory"])
        directory = self.__config["workDirectory"]
        filename  = str(int(round(time() * 1000)))+".csv"
        processor._createCSVWriter(directory, filename)
        
        self.assertTrue(os.path.exists(directory+"/"+filename,), "文件创建不成功")
        processor._backupFunction()
        self.assertFalse(os.path.exists(directory+"/"+filename,), "文件备份不成功")
        self.assertTrue(os.path.exists(self.__config["backupDirectory"]+"/"+filename,), "文件创建不成功")
        
    def testProcessWithSingleMetricValue(self):
        '''
                测试SingleMetricValue处理
        '''
        processor = CSVMetricProcessor(self.__config["workDirectory"],self.__config["backupDirectory"])
        metricValue = SingleMetricValue("cpu","count",4)
        processor.process(metricValue)
        
        timestemp = metricValue.getSampleTime()
        metricValue = SingleMetricValue("cpu","count",3)
        processor.process(metricValue)
        filePath = self.__config["workDirectory"]+"/"+ str(timestemp)+".csv"
        self.assertTrue(os.path.exists(filePath),"数据没有写入")
        fp = open(filePath,"r")
        reader = csv.reader(fp)
        
        index = 1;
        for line in reader:
            if len(line) == 0:
                continue
            self.assertEqual(1, len(line), "写入数据不正确")
            if index == 1:
                self.assertEqual("count", line[0], "写入数据不正确")
            elif index == 2:
                self.assertEqual("4", line[0], "写入数据不正确")
            elif index == 3:
                self.assertEqual("3", line[0], "写入数据不正确")
            index = index+1
        self.assertEqual(3, index-1, "写入数据行数不正确")
        fp.close()
    
    def testProcessWithMultiMetricValue(self):
        '''
                测试MultiMetricValue处理
        '''
        processor = CSVMetricProcessor(self.__config["workDirectory"],self.__config["backupDirectory"])
        metricValue = MultiMetricValue("cpu")
        metricValue.addMetricValue("count1", 1)
        metricValue.addMetricValue("count2", 2)
        metricValue.addMetricValue("count3", 3)
        metricValue.addMetricValue("count4", 4)
        processor.process(metricValue)
        timestemp = metricValue.getSampleTime()
        
        metricValue = MultiMetricValue("cpu")
        metricValue.addMetricValue("count1", 1)
        metricValue.addMetricValue("count2", 2)
        metricValue.addMetricValue("count3", 3)
        metricValue.addMetricValue("count4", 4)
        processor.process(metricValue)
        
        filePath = self.__config["workDirectory"]+"/"+ str(timestemp)+".csv"
        self.assertTrue(os.path.exists(filePath),"数据没有写入")
        fp = open(filePath,"r")
        reader = csv.reader(fp)
        
        index = 1;
        for line in reader:
            if len(line) == 0:
                continue
            self.assertEqual(4, len(line), "写入数据不正确")
            data = None
            if index == 1:
                data = ["count4","count3","count2","count1"]   
            elif index == 2:
                data = ["1","2","3","4"]
            elif index == 3:
                data = ["1","2","3","4"]
            success = True
            for ele in data:
                if ele in line:
                    pass
                else:
                    success = False;
            self.assertTrue(success, "写入数据不正确")
            index = index+1
        fp.close()
    def testProcessWithBatchMultiMetricValue(self):
        '''
                测试BatchMultiMetricValue处理
        '''
        processor = CSVMetricProcessor(self.__config["workDirectory"],self.__config["backupDirectory"])
        batchMultiMetricValue = BatchMultiMetricValue("cpu")
        metricValue = MultiMetricValue("cpu")
        metricValue.addMetricValue("count1", 1)
        metricValue.addMetricValue("count2", 2)
        batchMultiMetricValue.addMetricValue(metricValue)
        metricValue = MultiMetricValue("cpu")
        metricValue.addMetricValue("count1", 3)
        metricValue.addMetricValue("count2", 4)
        batchMultiMetricValue.addMetricValue(metricValue)

        processor.process(batchMultiMetricValue)
        
        timestemp = metricValue.getSampleTime()
        filePath = self.__config["workDirectory"]+"/"+ str(timestemp)+".csv"
        self.assertTrue(os.path.exists(filePath),"数据没有写入")
        fp = open(filePath,"r")
        reader = csv.reader(fp)
        index = 1;
        for line in reader:
            if len(line) == 0:
                continue
            self.assertEqual(3, len(line), "写入数据不正确")
            data = None
            if index == 1:
                data = ["batch-index","count1","count2"]   
            elif index == 2:
                data = ["1","1","2"]
            elif index == 3:
                data = ["2","3","4"]
            success = True
            for ele in data:
                if ele in line:
                    pass
                else:
                    success = False;
            self.assertTrue(success, "写入数据不正确")
            index = index+1
        fp.close()
        
    def testProcessWithKeyedMultiMetricValue(self):
        '''
                测试KeyedMultiMetricValue处理
        '''
        processor = CSVMetricProcessor(self.__config["workDirectory"],self.__config["backupDirectory"])
        keyedMultiMetricValue = KeyedMultiMetricValue("cpu")
        metricValue = MultiMetricValue("cpu")
        metricValue.addMetricValue("count1", 1)
        metricValue.addMetricValue("count2", 2)
        keyedMultiMetricValue.addMetricValue("key1",metricValue)
        metricValue = MultiMetricValue("cpu")
        metricValue.addMetricValue("count1", 3)
        metricValue.addMetricValue("count2", 4)
        keyedMultiMetricValue.addMetricValue("key2",metricValue)

        processor.process(keyedMultiMetricValue)
        
        timestemp = metricValue.getSampleTime()
        filePath = self.__config["workDirectory"]+"/"+ str(timestemp)+".csv"
        self.assertTrue(os.path.exists(filePath),"数据没有写入")
        fp = open(filePath,"r")
        reader = csv.reader(fp)
        index = 1;
        for line in reader:
            if len(line) == 0:
                continue
            self.assertEqual(3, len(line), "写入数据不正确")
            data = None
            if index == 1:
                data = ["keyed-index","count1","count2"]   
            else:
                data = ["key1","1","2","key2","3","4"]
            success = True
            for ele in line:
                if ele in data:
                    pass
                else:
                    success = False;
            self.assertTrue(success, "写入数据不正确")
            index = index+1
        fp.close()
        
    
    #测试入口
    if __name__ == "__main__":
        unittest.main()