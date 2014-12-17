# -*- coding: utf-8 -*-
'''
监控数据写入csv文件
参数配置：
    workDirectory  ：工作目录
    backupDirectory：备份目录
    backupInterval：备份间隔，默认30分钟
    headers：自定义header，没有配置则取metricvalue中的key作为header，默认没有配置
create on 2014-12-8
@author: liangzonghua
'''
from apscheduler.scheduler import Scheduler
from core.MetricProcessor import MetricProcessor
from core.MetricValue import SingleMetricValue, MultiMetricValue, BatchMultiMetricValue, KeyedMultiMetricValue
import csv
import os
import shutil
import threading

from monitor.utils.Logger import info, warn

KEY_BATCH_INDEX = "batch-index"
KEY_KEYED_INDEX = "keyed-index"
DEFAULT_BACKUP_INTERVAL = 30*60
class CSVMetricProcessor(MetricProcessor):
    
    __backupSched = None
    __csvFile = None
    __csvWriter=None
    
    def __init__(self, workDirectory, backupDirectory, backupInterval=DEFAULT_BACKUP_INTERVAL, headers=[]):
        '''
                初始化函数
        '''
        assert workDirectory != None and workDirectory != "", "没有配置CSV工作目录"
        assert backupDirectory != None and backupDirectory != "", "没有配置CSV备份目录"
        # 工作目录
        self.__workDirectory = workDirectory.replace("\\", "/")
        if os.path.exists(self.__workDirectory):
            pass
        else:
            os.makedirs(self.__workDirectory)
        # 备份目录
        self.__backupDirectory = backupDirectory.replace("\\", "/")
        if os.path.exists(self.__backupDirectory):
            pass
        else:
            os.makedirs(self.__backupDirectory)
        # 备份间隔   
        if backupInterval > 0:
            self.__backupInterval = backupInterval
        else:
            self.__backupInterval = DEFAULT_BACKUP_INTERVAL    
        # 自定义header
        self.__headers = headers
        # 锁初始化
        self.__lock = threading.RLock()


    def _backupFunction(self):
        '''
                备份策略
        '''
        assert os.path.exists(self.__workDirectory) and os.path.isdir(self.__workDirectory), "CSV工作目录不存在"
        assert os.path.exists(self.__backupDirectory) and os.path.isdir(self.__backupDirectory), "CSV备份目录不存在"
        self.__lock.acquire(True)
        # 关闭流
        if self.__csvFile != None:
            self.__csvFile.close()
            self.__csvFile = None
        info("开始备份[" + self.__workDirectory + "-->" + self.__backupDirectory + "]...")
        files = os.listdir(self.__workDirectory)
        if files == None or len(files) == 0:
            info("没有找到文件，备份结束")
            pass
        else:
            for file in files:
                src = self.__workDirectory + "/" + file
                if os.path.isfile(src):
                    dest = self.__backupDirectory + "/" + file
                    shutil.move(src, dest)
                    info("移动文件:[" + src + "-->" + dest + "]")
            info("备份结束.") 
        self.__lock.release()
        
    def start(self):
        '''
                处理器启动
        '''
        #启动备份器
        sched = Scheduler()
        sched.add_interval_job(self._backupFunction, seconds=self.__backupInterval)
        sched.daemonic = False
        sched.start()
        self.__sched = sched
        
    def stop(self):
        '''
                处理器停止
        '''
        self.__lock.acquire(True)
        if self.__backupSched != None:
            self.__backupSched.shutdown()
        if self.__csvFile != None:
            self.__csvFile.close()
            self.__csvFile = None
        if self.__csvWriter !=None:
            self.__csvWriter = None
        MetricProcessor.stop(self)
        self.__lock.release()
        
    
    def process(self, metricValue):
        '''
               处理函数
        '''
        sampleTime = metricValue.getSampleTime()
        #clientId = metricValue.getClientId();
        #monitorSourceName = metricValue.getMonitorSourceName();
        #加锁
        self.__lock.acquire(True)
        writer = None
        try:
            directory = self.__workDirectory
            writer = None
            if self.__csvFile == None:
                writer = self._createCSVWriter(directory, str(sampleTime)+".csv")
                self.__csvWriter = writer
            else:
                writer = self.__csvWriter
            #根据不同的metricValue采用不同的处理方法
            if isinstance(metricValue, SingleMetricValue):
                self._processSingleMetricValue(writer, metricValue)
            elif isinstance(metricValue, MultiMetricValue):
                self._processMultiMetricValue(writer, metricValue)
            elif isinstance(metricValue, BatchMultiMetricValue):
                self._processBatchMultiMetricValue(writer, metricValue)
            elif isinstance(metricValue, KeyedMultiMetricValue):
                self._processKeyedMultiMetricValue(writer, metricValue)
            else:
                warn("未知类型MetricValue")
        except Exception:
            raise Exception("写入CSV文件出错")
        finally:
            #释放锁
            self.__lock.release()
    
    def _processSingleMetricValue(self, writer, singleMetricValue):  
        name = singleMetricValue.getMetricName()
        if self.__headers == None or len(self.__headers) == 0:
            self.__headers = [name]
        if self.__isNewFile:
            writer.writerow(self.__headers)
            self.__isNewFile = False
        writer.writerow([str(singleMetricValue.getMetricValue())])
        self.__csvFile.flush()
    
    def _processMultiMetricValue(self, writer, multiMetricValue):
        values = multiMetricValue.getValues()
        if values == None or len(values) == 0:
            return None
        if self.__headers == None or len(self.__headers) == 0:
            self.__headers = list(values.keys())
        if self.__isNewFile:
            writer.writerow(self.__headers)
            self.__isNewFile = False
            
        metricValues = []
        for key in self.__headers:
            metricValues.append(multiMetricValue.getValue(key))
        writer.writerow(metricValues)
        self.__csvFile.flush()
        
    def _processBatchMultiMetricValue(self, writer, batchMultiMetricValue):
        arrayValues = batchMultiMetricValue.getValues()
        if arrayValues == None or len(arrayValues) == 0:
            return None
        if self.__headers == None or len(self.__headers) == 0:
            self.__headers = list(arrayValues[0].getValues().keys())
            self.__headers.insert(0, KEY_BATCH_INDEX)
        if self.__isNewFile:
            writer.writerow(self.__headers)
            self.__isNewFile = False
        index = 1;
        for multiMetricValue in arrayValues:
            metricValues = [index]
            if multiMetricValue == None:
                pass
            else:
                for key in self.__headers:
                    if key == KEY_BATCH_INDEX:
                        continue
                    else:
                        metricValues.append(multiMetricValue.getValue(key))
            writer.writerow(metricValues)
            index = index+1
        self.__csvFile.flush()
    
    def _processKeyedMultiMetricValue(self, writer, keyedMultiMetricValue):
        dictValues = keyedMultiMetricValue.getValues()
        if dictValues == None or len(dictValues) == 0:
            return None
       
        for key in dictValues:
            values = dictValues[key]
            if self.__headers == None or len(self.__headers) == 0:
                self.__headers = list(dictValues[key].getValues().keys())
                self.__headers.insert(0, KEY_KEYED_INDEX)
            if self.__isNewFile:
                writer.writerow(self.__headers)
                self.__isNewFile = False
            metricValues = [key]
            for kk in self.__headers:
                if kk == KEY_KEYED_INDEX:
                    continue
                else:
                    metricValues.append(values.getValue(kk))
            writer.writerow(metricValues)            
        self.__csvFile.flush()
    
    def _createCSVWriter(self, directory, fileName):
        self.__lock.acquire(True)
        f = None
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        files = os.listdir(directory)
        if files == None or len(files) == 0:
            f = directory + "/" + fileName
            self.__isNewFile = True
        else:
            f = directory + "/" + files[0]
            self.__isNewFile = False
        self.__csvFile = open(f, 'a')
        self.__lock.release()
        return csv.writer(self.__csvFile)