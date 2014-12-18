'''
Created on 2014-11-10

'''

from builtins import print
import logging

from config import config


logging.basicConfig(filename=config.loggerFileName, level=logging.DEBUG)

def debug(msg):
    logging.debug(msg)
    print(msg)

def info(msg):
    logging.info(msg)
    print(msg)

def warn(msg):
    logging.warning(msg)
    print(msg)
    
def error(msg):
    logging.warning(msg)
    print(msg)
    
def fatal(msg):
    logging.fatal(msg)
    print(msg)
    