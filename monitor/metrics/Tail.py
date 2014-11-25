'''
Created on 2014-11-15
reference:http://wolfchen.blog.51cto.com/2211749/1374470
@author: hongye
'''

import re
import threading
import time
import traceback

from core.MetricValue import MultiMetricValue
from core.MonitorSource import ObserableMonitorSource


class Tailer(object):
    """\
    Implements tailing and heading functionality like GNU tail and head
    commands.
    """
    line_terminators = ('\r\n', '\n', '\r')

    def __init__(self, file, read_size=1024, end=False):
        self.read_size = read_size
        self.file = file
        self.start_pos = self.file.tell()
        if end:
            self.seek_end()
    
    def splitlines(self, data):
        return re.split('|'.join(self.line_terminators), data)

    def seek_end(self):
        self.seek(0, 2)

    def seek(self, pos, whence=0):
        self.file.seek(pos, whence)

    def read(self, read_size=None):
        if read_size:
            read_str = self.file.read(read_size)
        else:
            read_str = self.file.read()

        return len(read_str), read_str

    def seek_line_forward(self):
        """\
        Searches forward from the current file position for a line terminator
        and seeks to the charachter after it.
        """
        pos = start_pos = self.file.tell()

        bytes_read, read_str = self.read(self.read_size)

        start = 0
        if bytes_read and read_str[0] in self.line_terminators:
            # The first charachter is a line terminator, don't count this one
            start += 1

        while bytes_read > 0:          
            # Scan forwards, counting the newlines in this bufferfull
            i = start
            while i < bytes_read:
                if read_str[i] in self.line_terminators:
                    self.seek(pos + i + 1)
                    return self.file.tell()
                i += 1

            pos += self.read_size
            self.seek(pos)

            bytes_read, read_str = self.read(self.read_size)

        return None

    def seek_line(self):
        """\
        Searches backwards from the current file position for a line terminator
        and seeks to the charachter after it.
        """
        pos = end_pos = self.file.tell()

        read_size = self.read_size
        if pos > read_size:
            pos -= read_size
        else:
            pos = 0
            read_size = end_pos

        self.seek(pos)

        bytes_read, read_str = self.read(read_size)

        if bytes_read and read_str[-1] in self.line_terminators:
            # The last charachter is a line terminator, don't count this one
            bytes_read -= 1

            if read_str[-2:] == '\r\n' and '\r\n' in self.line_terminators:
                # found crlf
                bytes_read -= 1

        while bytes_read > 0:          
            # Scan backward, counting the newlines in this bufferfull
            i = bytes_read - 1
            while i >= 0:
                if read_str[i] in self.line_terminators:
                    self.seek(pos + i + 1)
                    return self.file.tell()
                i -= 1

            if pos == 0 or pos - self.read_size < 0:
                # Not enought lines in the buffer, send the whole file
                self.seek(0)
                return None

            pos -= self.read_size
            self.seek(pos)

            bytes_read, read_str = self.read(self.read_size)

        return None
  
    def tail(self, lines=10):
        """\
        Return the last lines of the file.
        """
        self.seek_end()
        end_pos = self.file.tell()

        for i in range(lines):
            if not self.seek_line():
                break

        data = self.file.read(end_pos - self.file.tell() - 1)
        if data:
            return self.splitlines(data)
        else:
            return []
               
    def head(self, lines=10):
        """\
        Return the top lines of the file.
        """
        self.seek(0)

        for i in range(lines):
            if not self.seek_line_forward():
                break
    
        end_pos = self.file.tell()
        
        self.seek(0)
        data = self.file.read(end_pos - 1)

        if data:
            return self.splitlines(data)
        else:
            return []

    def follow(self, delay=1.0):
        """\
        Iterator generator that returns lines as data is added to the file.
        Based on: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/157035
        """
        trailing = True       
        
        while 1:
            where = self.file.tell()
            line = self.file.readline()
            if line:    
                if trailing and line in self.line_terminators:
                    # This is just the line terminator added to the end of the file
                    # before a new line, ignore.
                    trailing = False
                    continue

                if line[-1] in self.line_terminators:
                    line = line[:-1]
                    if line[-1:] == '\r\n' and '\r\n' in self.line_terminators:
                        # found crlf
                        line = line[:-1]

                trailing = False
                yield line
            else:
                trailing = True
                self.seek(where)
                time.sleep(delay)

    def __iter__(self):
        return self.follow()

    def close(self):
        self.file.close()

class TailThread(threading.Thread):
    _parent = None
    _filepath = None
    tailer = None
    
    def __init__(self, filepath, parent):
        self._parent = parent
        self._filepath = filepath
        threading.Thread.__init__(self)
        self.t_name = "tail_" + filepath
        self.tailer = Tailer(open(self._filepath, 'rb'))
       
    def run(self): 
        try:
            try:
#                 if options.lines > 0:
#                     if options.head:
#                         if options.follow:
#                             sys.stderr.write('Cannot follow from top of file.\n')
#                             sys.exit(1)
#                         lines = tailer.head(options.lines)
#                     else:
#                         lines = tailer.tail(options.lines)
#             
#                     for line in lines:
#                         print(line)
#                 elif options.follow:
#                     # Seek to the end so we can follow
                self.tailer.seek_end()
                for line in self.tailer.follow(delay=1.0):
                    try:
                        self._parent.process(line)
                    except:
                        print(traceback.format_exc())
                        break
            except KeyboardInterrupt:
                # Escape silently
                pass
        finally:
            self.tailer.close()


class LineParser(object):
    def parse(self,line):
        pass

class TailMonitorSource(ObserableMonitorSource):
    _file = None
    _interval = 1
    _lineParser = None
    _tailThread = None
    
    def start(self):
        self._tailThread = TailThread(self._file, self)
        self._tailThread.start()
        
    def process(self, line):
        values = self._lineParser.parse(line.decode())
        if values == None:
            return ;
        metricValue = MultiMetricValue(self.getMonitorSourceName())
        metricValue.addMetricValues(values)
        self.notify(metricValue)
        
    def stop(self):
        self._tailThread.stop()
        
    def fail(self):
        pass
    
    def file(self, file):
        self._file = file
        return self
    def lineParser(self,lineParser):
        self._lineParser = lineParser
        return self
    