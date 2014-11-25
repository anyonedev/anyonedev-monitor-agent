'''
Created on 2014-11-18

@author: hongye
'''
import re
import time

from metrics.log.AgentParser import detect


class NginxAccessLogLineParser(object):
    ipP = r"?P<ip>[\d.]*"
    timeP = r"""?P<time>\[[^\[\]]*\]"""
    requestP = r"""?P<request>\"[^\"]*\""""
    statusP = r"?P<status>\d+"
    bodyBytesSentP = r"?P<bodyByteSent>\d+"
    referP = r"""?P<refer>\"[^\"]*\""""
    userAgentP = r"""?P<userAgent>\"[^\"]*\""""
    userOperatorSystems = re.compile(r'\([^\(\)]*\)')
    userBrowers = re.compile(r'[^\)]*\"')
    nginxLogPattern = re.compile(r"(%s)\ -\ -\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)" % (ipP, timeP, requestP, statusP, bodyBytesSentP, referP, userAgentP), re.VERBOSE) 
    
    def parse(self, line):
        matchs = self.nginxLogPattern.match(line)
        if matchs != None:
            values = dict()
            groups = matchs.groups()
            values["ip"] = groups[0]
            values["request"] = groups[2]
            values["status"] = groups[3]
            values["body_bytes_sent"] = groups[4]
            values["refer"] = groups[5]
            
            userAgent = groups[6]
            values["user_agent"] = userAgent
            
            t = groups[1]
            if t != None:
                values["time"] = int(time.mktime(time.strptime(t, '[%d/%b/%Y:%H:%M:%S %z]')))
            
            if len(userAgent) > 20:
                agent = detect(userAgent)
                os = agent.get("os")
                if os != None:
                    values["os_name"] = os.get("name")
                    values["os_version"] = os.get("version")
                
                if agent.get("bot") != None:
                    values["is_bot"] = agent.get("bot")
                
                browser = agent.get("browser")
                if browser != None:
                    values["browser_name"] =browser.get("name")
                    values["browser_version"] = browser.get("version")
                
                platform = agent.get("platform")
                if platform != None:
                    values["platform_name"] = platform.get("name")
                    values["platform_version"] = platform.get("version")
            return values
        return None

def nginx_access_log_parser():
    return NginxAccessLogLineParser()
      
