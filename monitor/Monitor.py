'''
Created on 2014-11-12

@author: 
'''

__version__ = "1.0.0.dev"

from boostrap import Boostrap
from utils import Logger


if __name__ == '__main__':
    Logger.info("init the anyonedev monitor service agent")
    main = Boostrap.Boostrap()
    main.start()
    Logger.info("init finish the anyonedev monitor service agent")
    