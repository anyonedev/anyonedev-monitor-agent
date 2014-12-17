#!/usr/bin/python -O

import re
import sys
import json
from monitor.metrics.Tail import LineParser

"""
This is a parser of GC log of Sun HotSpot JVM Version 6.

Required JVM option: -Xloggc=${GC_LOG_FILE} -XX:+PrintGCDetails

Usage:
   java -Xloggc=${GC_LOG_FILE} -XX:+PrintGCDetails ${ANY_OTHER_OPTIONS}
   this.py < ${GC_LOG_FILE} | grep -v ^### | ${YOUR_ANALYZER}

You can get all data as a python dictionary structure
in your analyer as follows:

look at testcase in test.metrics.log.GCLoggerTest.py
        
"""

################################################################################
# Parser generator from regular expression.
################################################################################

"""
Generate a parser from regex pattern and modifier.

Parser try to match input text by the pattern.
If matched, call data_modifier with list of matched strings.
The modifier add/update tag_str of the dictionary.

regexStr :: String
dataModifier :: (a, [String]) -> a | None
return :: (String, a) -> (String, a)
a :: ANY

dataModifier must not throw exceptions.
When some errors occur inside dataModifier, a must be not modified.

"""
def newP(regexStr, dataModifier):
    p = re.compile("(^%s)" % regexStr)
    def parse_(line, data):
        m = p.match(line)
        if m:
            if dataModifier is not None:
                data = dataModifier(data, m.groups()[1:])
            return (line[len(m.group(1)):], data)
        else:
            msg = "Parse failed: pattern \"%s\" for \"%s\"" % (regexStr, line)
            raise ParseError(msg)
    return parse_

################################################################################
# Utilities.
################################################################################

"""
Just modify data during parse.

dataModifier :: (a, [String]) -> a
return :: (String, a) -> (String, a)
a :: ANY

"""
def appP(dataModifier):
    def modify_(line, data):
        if dataModifier is not None:
            data = dataModifier(data)
        return (line, data)
    return modify_


# [String] -> String
def toString(strL):
    ret = "[%s" % strL[0]
    for str in strL[1:]:
        ret += ", %s" % str
    ret += "]"
    return ret


# Error type for parser.
class ParseError(Exception):
    pass


################################################################################
# Parser combinators.
################################################################################

"""
Parser combinator AND.

parsers :: [Parser]
return :: Parser

"""
def andP(parsers):
    def parseAnd_(text, data):
        text0 = text
        data0 = data
        for parser in parsers:
            (text1, data1) = parser(text0, data0)
            text0 = text1
            data0 = data1
        return (text0, data0)
    return parseAnd_

"""
Parser combinator OR.

parsers :: [Parser]
return :: Parser

"""
def orP(parsers):
    def parseOr_(text, data):
        msgL = []
        for parser in parsers:
            try:
                (ret_text, ret_data) = parser(text, data)
                return (ret_text, ret_data)
            except ParseError as msg:
                msgL.append(msg)
        msgs = toString(msgL)
        raise ParseError(msgs)
    return parseOr_

"""
Parser combinator MANY.
parsers :: [Parser]
return :: Parser

"""
def manyP(parser):
    def parseMany_(text, data):
        text0 = text
        data0 = data
        text1 = text
        data1 = data
        try:
            while True:
                (text1, data1) = parser(text0, data0)
                text0 = text1
                data0 = data1
        except ParseError as msg:
            if __debug__:
                print(msg)
        return (text1, data1)
    return parseMany_


################################################################################
# Utilities.
################################################################################

"""
A modifier for dictionary data.

tagStr :: String
dataConstructor :: [String] -> ANY
return :: (Dictionary, [String]) -> Dictionary

"""
def mkDictModifier(tagStr, dataConstructor):
    def modifyNothing_(dictData, matchStringL):
        return dictData
    if tagStr is None or dataConstructor is None:
        return modifyNothing_
    def modifyDict_(dictData, matchStringL):
        dictData[tagStr] = dataConstructor(matchStringL)
        return dictData
    return modifyDict_

"""
Behave like newP but that parses anything, just modify dictionary.

key :: String
value :: ANY
return :: (String, Dictionary) -> (String, Dictionary)

"""
def mkTagger(key, value):
    def tagger_(line, dictData):
        dictData[key] = value
        return (line, dictData)
    return tagger_


# match_strL :: [String] # length must be 1.
# return :: Float
def get_float(match_strL):
    assert len(match_strL) == 1
    return float(match_strL[0])

# match_strL :: [String] # length must be 3.
# return :: [Int] # length is 3.
def get_int3(match_strL):
    assert len(match_strL) == 3
    return [int(match_strL[0]), int(match_strL[1]), int(match_strL[2])]

# match_strL :: [String]
# return :: True
def get_true(match_strL):
    return True


################################################################################
# Regexp aliases.
################################################################################

regexp_float = r"(\d+.\d*)"
regexp_float_colon = regexp_float + r":\s+"
regexp_heap_info = r"(\d+)K->(\d+)K\((\d+)K\)"
regexp_float_secs = regexp_float + r"\s*secs\s+"
regexp_basic_string = r"([0-9a-zA-Z_-]+)"


################################################################################
# Parsers for gc log entries.
################################################################################

parseParNew = andP([ \
    mkTagger("type", "ParNew"), \
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)), \
    newP(r"\[GC\s+", None), \
    newP(regexp_float_colon, None), \
    newP(r"\[ParNew:\s+", None), \
    newP(regexp_heap_info + r",\s+", mkDictModifier("heap_new", get_int3)), \
    newP(regexp_float + r"\s*secs\]\s*", None), \
    newP(regexp_heap_info, mkDictModifier("heap_all", get_int3)), \
    newP(r"\s*(?:icms_dc=\d+\s*)?", None), \
    newP(r",\s*", None), \
    newP(regexp_float + r"\s*secs\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"2.380: [GC 2.380: [ParNew: 32768K->4204K(49152K), 0.0128980 secs] 32768K->4204K(114688K), 0.0130090 secs] [Times: user=0.04 sys=0.00, real=0.01 secs]"
    (ret, data) = parseParNew(text, {})
    print(text)
    print(len(ret))
    print(data)
if __debug__:
    text = r"9.815: [GC 9.815: [ParNew: 32768K->10796K(49152K), 0.0286700 secs] 52540K->30568K(114688K) icms_dc=0 , 0.0287550 secs] [Times: user=0.09 sys=0.00, real=0.03 secs]"
    (ret, data) = parseParNew(text, {})
    print(text)
    print(len(ret))
    print(data)
'''   

parseInitialMark = andP([ \
    mkTagger("type", "CMS-initial-mark"), \
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)), \
    newP(r".*CMS-initial-mark:.*$", None), \
])
'''
if __debug__:
    text = r"3.072: [GC [1 CMS-initial-mark: 0K(65536K)] 19136K(114688K), 0.0215880 secs] [Times: user=0.04 sys=0.00, real=0.02 secs]"
    (ret, data) = parseInitialMark(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseMarkStart = andP([ \
    mkTagger("type", "CMS-concurrent-mark-start"), \
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)), \
    newP(r".*CMS-concurrent-mark-start.*$", None), \
])
'''
if __debug__:
    text = r"3.094: [CMS-concurrent-mark-start]"
    (ret, data) = parseMarkStart(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseMark = andP([ \
    mkTagger("type", "CMS-concurrent-mark"), \
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)), \
    newP(r"\[CMS-concurrent-mark:\s+", None), \
    newP(regexp_float + r"/", None), \
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"3.131: [CMS-concurrent-mark: 0.034/0.037 secs] [Times: user=0.12 sys=0.00, real=0.04 secs]"
    (ret, data) = parseMark(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parsePrecleanStart = andP([ \
    mkTagger("type", "CMS-concurrent-preclean-start"), \
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)), \
    newP(r".*CMS-concurrent-preclean-start.*$", None), \
])
'''
if __debug__:
    text = r"3.132: [CMS-concurrent-preclean-start]"
    (ret, data) = parsePrecleanStart(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parsePreclean = andP([ \
    mkTagger("type", "CMS-concurrent-preclean"), \
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)), \
    newP(r"\[CMS-concurrent-preclean:\s+", None), \
    newP(regexp_float + r"/", None), \
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"3.149: [CMS-concurrent-preclean: 0.014/0.018 secs] [Times: user=0.07 sys=0.00, real=0.01 secs]"
    (ret, data) = parsePreclean(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseAbortablePrecleanStart = andP([ \
    mkTagger("type", "CMS-concurrent-abortable-preclean-start"), \
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)), \
    newP(r".*CMS-concurrent-abortable-preclean-start.*$", None), \
])
'''
if __debug__:
    text = r"3.149: [CMS-concurrent-abortable-preclean-start]"
    (ret, data) = parseAbortablePrecleanStart(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseAbortablePreclean = andP([ \
    mkTagger("type", "CMS-concurrent-abortable-preclean"), \
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)), \
    newP(r"\[CMS-concurrent-abortable-preclean:\s+", None), \
    newP(regexp_float + r"/", None), \
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"17.418: [CMS-concurrent-abortable-preclean: 0.353/1.423 secs] [Times: user=4.60 sys=0.07, real=1.42 secs]"
    (ret, data) = parseAbortablePreclean(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseAbortablePrecleanFullGC0 = andP([ \
    mkTagger("type", "CMS-concurrent-abortable-preclean-fullgc0"), \
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)), \
    orP([ \
      newP(r"\[Full GC\s*\(System\)\s*" + regexp_float + r":\s+", mkDictModifier("system", get_true)), \
      newP(r"\[Full GC\s*" + regexp_float + r":\s+", None), \
    ]), \
    newP(r"\[CMS" + regexp_float + r":\s+", None), \
    newP(r"\[CMS-concurrent-abortable-preclean:\s+", None), \
    newP(regexp_float + r"/", None), \
    newP(regexp_float + r"\s+secs\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"3.242: [Full GC 3.242: [CMS3.243: [CMS-concurrent-abortable-preclean: 0.046/0.093 secs] [Times: user=0.36 sys=0.00, real=0.10 secs]"
    (ret, data) = parseAbortablePrecleanFullGC0(text, {})
    print(text)
    print(len(ret))
    print(data)
    text = r"63.533: [Full GC (System) 63.533: [CMS63.534: [CMS-concurrent-abortable-preclean: 0.316/1.244 secs] [Times: user=0.32 sys=0.01, real=1.25 secs]"
    (ret, data) = parseAbortablePrecleanFullGC0(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseAbortablePrecleanFullGC1 = andP([ \
    mkTagger("type", "CMS-concurrent-abortable-preclean-fullgc1"), \
    newP(r"\s*\(concurrent mode (failure|interrupted)\):\s+", None), \
    newP(regexp_heap_info + r",\s+", mkDictModifier("heap_1", get_int3)), \
    newP(regexp_float + r"\s+secs\s*\]\s+", None), \
    newP(regexp_heap_info + r",\s+", mkDictModifier("heap_2", get_int3)), \
    newP(r"\[CMS Perm\s+:\s+", None), \
    newP(regexp_heap_info + r"\],\s+", mkDictModifier("perm", get_int3)), \
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"  (concurrent mode failure): 0K->7015K(65536K), 0.1244810 secs] 22902K->7015K(114688K), [CMS Perm : 21242K->21237K(21248K)], 0.1246890 secs] [Times: user=0.19 sys=0.05, real=0.13 secs]"
    (ret, data) = parseAbortablePrecleanFullGC1(text, {})
    print(text)
    print(len(ret))
    print(data)
    text = r"  (concurrent mode interrupted): 44784K->40478K(65536K), 0.4974690 secs] 66630K->40478K(114688K), [CMS Perm : 77174K->77148K(128736K)], 0.4975800 secs] [Times: user=0.46 sys=0.03, real=0.50 secs]"
    (ret, data) = parseAbortablePrecleanFullGC1(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseAbortablePrecleanFailureTime = andP([ \
    mkTagger("type", "CMS-concurrent-abortable-preclean-failure-time"), \
    newP(r"\s*CMS:\s*abort preclean due to time\s*", None), \
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)), \
    newP(r"\[CMS-concurrent-abortable-preclean:\s*", None), \
    newP(regexp_float + r"/", None), \
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r" CMS: abort preclean due to time 36.855: [CMS-concurrent-abortable-preclean: 1.280/5.084 secs] [Times: user=1.29 sys=0.00, real=5.09 secs]"
    (ret, data) = parseAbortablePrecleanFailureTime(text, {})
    print(text)
    print(len(ret))
    print(data)
    text = r"3.368: [GC [1 CMS-initial-mark: 7015K(65536K)] 7224K(114688K), 0.0004900 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]"
    (ret, data) = parseInitialMark(text, {})
    print(text)
    print(len(ret))
    print(data)
    text = r"3.428: [CMS-concurrent-mark: 0.059/0.060 secs] [Times: user=0.22 sys=0.00, real=0.06 secs]"
    (ret, data) = parseMark(text, {})
    print(text)
    print(len(ret))
    print(data)
    text = r"3.431: [CMS-concurrent-preclean: 0.002/0.002 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]"
    (ret, data) = parsePreclean(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseRemark = andP([ \
    mkTagger("type", "CMS-remark"), \
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)), \
    newP(r"\[GC\[YG occupancy.+CMS-remark:\s+\d+K\(\d+K\)\]\s*", None), \
    newP(r"\d+K\(\d+K\),\s*", None), \
    newP(regexp_float + r"\s*secs\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"3.431: [GC[YG occupancy: 1005 K (49152 K)]3.431: [Rescan (parallel) , 0.0080410 secs]3.439: [weak refs processing, 0.0000100 secs]3.439: [class unloading, 0.0014010 secs]3.441: [scrub symbol & string tables, 0.0032440 secs] [1 CMS-remark: 7015K(65536K)] 8021K(114688K), 0.0130490 secs] [Times: user=0.03 sys=0.00, real=0.02 secs]"
    (ret, data) = parseRemark(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseSweepStart = andP([ \
    mkTagger("type", "CMS-concurrent-sweep-start"), \
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)), \
    newP(r"\[CMS-concurrent-sweep-start\]$", None), \
])
'''
if __debug__:
    text = r"3.444: [CMS-concurrent-sweep-start]"
    (ret, data) = parseSweepStart(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseSweep = andP([ \
    mkTagger("type", "CMS-concurrent-sweep"), \
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)), \
    newP(r"\[CMS-concurrent-sweep:\s+", None), \
    newP(regexp_float + r"/", None), \
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"3.468: [CMS-concurrent-sweep: 0.024/0.024 secs] [Times: user=0.06 sys=0.00, real=0.02 secs]"
    (ret, data) = parseSweep(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseResetStart = andP([ \
    mkTagger("type", "CMS-concurrent-reset-start"), \
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)), \
    newP("\[CMS-concurrent-reset-start\]$", None), \
])
'''
if __debug__:
    text = r"3.468: [CMS-concurrent-reset-start]"
    (ret, data) = parseResetStart(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseReset = andP([ \
    mkTagger("type", "CMS-concurrent-reset"), \
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)), \
    newP(r"\[CMS-concurrent-reset:\s+", None), \
    newP(regexp_float + r"/", None), \
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"3.468: [CMS-concurrent-reset: 0.000/0.000 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]"
    (ret, data) = parseReset(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

parseFullGC = andP([ \
    mkTagger("type", "FullGC"), \
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)), \
    orP([ \
        newP(r"\[Full GC\s*\(System\)\s*", mkDictModifier("system", get_true)), \
        newP(r"\[Full GC\s*", None), \
    ]), \
    newP(regexp_float_colon, None), \
    newP(r"\[CMS:\s+", None), \
    newP(regexp_heap_info + r",\s+", mkDictModifier("heap_cms", get_int3)), \
    newP(regexp_float + r"\s*secs\]\s*", None), \
    newP(regexp_heap_info, mkDictModifier("heap_all", get_int3)), \
    newP(r"\s*,\s*\[CMS Perm\s*:\s*", None), \
    newP(regexp_heap_info, mkDictModifier("perm", get_int3)), \
    newP(r"\]\s*(?:icms_dc=\d+\s*)?", None), \
    newP(r",\s*", None), \
    newP(regexp_float + r"\s*secs\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"7.992: [Full GC 7.992: [CMS: 6887K->19772K(65536K), 0.4137230 secs] 34678K->19772K(114688K), [CMS Perm : 54004K->53982K(54152K)] icms_dc=0 , 0.4140100 secs] [Times: user=0.68 sys=0.14, real=0.41 secs]"
    (ret, data) = parseFullGC(text, {})
    print(text)
    print(len(ret))
    print(data)
    text = r"123.533: [Full GC (System) 123.533: [CMS: 39710K->34052K(65536K), 0.4852070 secs] 62832K->34052K(114688K), [CMS Perm : 77479K->76395K(128928K)], 0.4853310 secs] [Times: user=0.47 sys=0.01, real=0.48 secs]"
    (ret, data) = parseFullGC(text, {})
    print(text)
    print(len(ret))
    print(data)
'''
# This is for -XX:+UseParallelGC
parseParallelGC = andP([ \
    mkTagger("type", "ParallelGC"), \
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)), \
    newP(r"\[GC\s+\[PSYoungGen:\s*", None), \
    newP(regexp_heap_info + r"\s*\]\s*", mkDictModifier("heap_new", get_int3)), \
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_all", get_int3)), \
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"162.002: [GC [PSYoungGen: 39323K->3653K(49152K)] 87187K->56999K(114688K), 0.0207580 secs] [Times: user=0.08 sys=0.00, real=0.02 secs]"
    (ret, data) = parseParallelGC(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

# This is for -XX:+UseParallelGC
parseParallelFullGC = andP([ \
    mkTagger("type", "ParallelFullGC"), \
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)), \
    orP([ \
      newP(r"\[Full GC\s*\(System\)\s*\[PSYoungGen:\s*", mkDictModifier("system", get_true)), \
      newP(r"\[Full GC\s*\[PSYoungGen:\s*", None), \
    ]), \
    newP(regexp_heap_info + r"\s*\]\s*", mkDictModifier("heap_new", get_int3)), \
    orP([ \
         newP(r"\[ParOldGen:\s*", None), \
         newP(r"\[PSOldGen:\s*", None), \
    ]), \
    newP(regexp_heap_info + r"\s*\]\s*", mkDictModifier("heap_old", get_int3)), \
    newP(regexp_heap_info + r"\s*", mkDictModifier("heap_all", get_int3)), \
    newP(r"\[PSPermGen:\s*", None), \
    newP(regexp_heap_info + r"\s*\]\s*,\s*", mkDictModifier("perm", get_int3)), \
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"162.657: [Full GC [PSYoungGen: 6189K->0K(50752K)] [PSOldGen: 58712K->43071K(65536K)] 64902K->43071K(116288K) [PSPermGen: 81060K->81060K(81152K)], 0.3032230 secs] [Times: user=0.30 sys=0.00, real=0.30 secs]"
    (ret, data) = parseParallelFullGC(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

# This is for -XX:+UseSerialGC
parseSerialGC = andP([ \
    mkTagger("type", "SerialGC"), \
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)), \
    newP(r"\[GC\s+", None), \
    newP(regexp_float_colon + r"\[DefNew:\s*", None), \
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_new", get_int3)), \
    newP(regexp_float + r"\s*secs\s*\]\s*", None), \
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_all", get_int3)), \
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"4.687: [GC 4.687: [DefNew: 33343K->649K(49152K), 0.0021450 secs] 45309K->12616K(114688K), 0.0021800 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]"
    (ret, data) = parseSerialGC(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

# This is for -XX:+UseSerialGC
parseSerialFullGC = andP([ \
    mkTagger("type", "SerialFullGC"), \
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)), \
    newP(r"\[Full GC\s+", None), \
    newP(regexp_float_colon + r"\s*", None), \
    newP(r"\[Tenured:\s*", None), \
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_old", get_int3)), \
    newP(regexp_float + r"\s*secs\]\s*", None), \
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_all", get_int3)), \
    newP(r"\[Perm\s*:\s*", None), \
    newP(regexp_heap_info + r"\s*\]\s*,\s*", mkDictModifier("perm", get_int3)), \
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)), \
    newP(r"\[Times:.*\]$", None), \
])
'''
if __debug__:
    text = r"4.899: [Full GC 4.899: [Tenured: 11966K->12899K(65536K), 0.1237750 secs] 22655K->12899K(114688K), [Perm : 32122K->32122K(32128K)], 0.1238590 secs] [Times: user=0.11 sys=0.00, real=0.13 secs]"
    (ret, data) = parseSerialFullGC(text, {})
    print(text)
    print(len(ret))
    print(data)
'''

"""
Java GC Log parser.
This supports almost kinds of GC provided by JVM.

-XX:+UseConcSweepGC (-XX:+UseParNewGC)
 parseParNew
 parseFullGC

-XX:+UseConcSweepGC -XX:CMSIncrementalMode (-XX:+UseParNewGC)
 parseParNew, parseFullGC,
 parse{InitialMark, MarkStart, Mark, PrecleanStart, Preclean,
       AbortablePrecleanStart, AbortablePreclean,
       AbortablePrecleanFullGC0, AbortablePrecleanFullGC1,
       AbortablePrecleanFailureTime,
       Remark,
       SweepStart, Sweep, ResetStart, Reset}
  parseAbortablePrecleanFullGC0 and parseAbortablePrecleanFullGC1
  must be always together.

-XX:+UseParallelGC
  parseParallelFullGC, parseParallelGC.

-XX:+UseSerialGC
  parseSerialFullGC, parseSerialGC.
  
"""
parseJavaGcLog = orP([ \
    parseParNew, \
    parseFullGC, \
    parseInitialMark, \
    parseMarkStart, parseMark, \
    parsePrecleanStart, parsePreclean, \
    parseAbortablePrecleanStart, parseAbortablePreclean, \
    parseAbortablePrecleanFullGC0, \
    parseAbortablePrecleanFullGC1, 
    parseAbortablePrecleanFailureTime, \
    parseRemark, \
    parseSweepStart, parseSweep, \
    parseResetStart, parseReset, \
    parseParallelFullGC, \
    parseParallelGC, \
    parseSerialFullGC, \
    parseSerialGC, \
])


################################################################################
# Parser of list of integer. This is for test.
################################################################################

"""
A modifier for list.

return :: ([[String]], [String]) -> [String]

"""
def mkListAppender():
    def listAppend_(list, matchStringL):
        if len(matchStringL) > 0:
            list.append(matchStringL[0])
        return list
    return listAppend_

"""
Convert last element to Int.

list :: [Int, Int, ..., Int, String]
return :: [Int, Int, ..., Int, Int]

"""
def convertLastToInt(list):
    list[-1] = int(list[-1])
    return list

# Parser of list of integer. This is for test.
parseIntList = andP([ \
    newP(r"\s*\[\s*", None), \
    manyP(andP([ \
        newP("(\d+)\s*(?:,\s*)?", mkListAppender()), \
        appP(convertLastToInt), \
    ])), \
    newP(r"\s*\]\s*", None), \
])
'''
if __debug__:
    text = r"[10, 20, 30]"
    (ret, data) = parseIntList(text, [])
    print(text)
    print(len(ret))
    print(data)
'''
      
################################################################################
# main
################################################################################
class GCLogLineParser(LineParser):
    array_clazz = [].__class__
    def parse(self,line):
        (ret,data) = parseJavaGcLog(line, {})
        values = dict()
        if not isinstance(data, dict):
            return None
        for key,value in data.items():
            if isinstance(value, self.array_clazz) and len(value) == 3:
                values[key+"-before"]=value[0]
                values[key+"-after"]=value[1]
                values[key+"-total"]=value[2]
            else:
                values[key] = value
        return values  
    
'''
data_prev = None
for line in sys.stdin:
    try:
        text = line.rstrip()
        #print(text)
        (ret, data) = parseJavaGcLog(text, {})
        if data["type"] == "CMS-concurrent-abortable-preclean-fullgc0":
            data_prev = data
            continue
        if data["type"] == "CMS-concurrent-abortable-preclean-fullgc1":
            assert data_prev["type"] == "CMS-concurrent-abortable-preclean-fullgc0"
            data_prev.update(data)
            data = data_prev
            data_prev = None
            data["type"] = "CMS-concurrent-abortable-preclean-fullgc"
        if __debug__:
            print(("len: %d" % len(ret)))
        print(json.dumps(data))
    except ParseError as msg:
        print(msg)
        print(("###%s" % text))

'''
# end of file.