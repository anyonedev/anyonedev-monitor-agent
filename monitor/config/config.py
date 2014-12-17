'''
Created on 2014-11-12

@author: hongye
'''

from os import getcwd


clientId = "outworker"
version = "1.0.0"
home = getcwd()
loggerFileName = "out.log"

influxDBSender = {"host":"localhost",
            "username":"root",
            "password":"root",
            "port":8086,
            "database":"logs"}

mysqlConfig = {
        'host': 'localhost',
        'port': 3306,
        'database': 'common_schema',
        'user': 'root',
        'password': '123456',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
    }

graphiteSender = {
    "Carbon_LineReceiverHost"  : "localhost",
    "Carbon_LineReceiverPort" : 2003,
    "Carbon_LineReceiverProtocol":"tcp",  
    }