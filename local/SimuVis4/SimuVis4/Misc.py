# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""Misc - misc. general functions and classes"""

import os, time, stat, re, select


### Misc. Objects and calling...


class DictProxy(object):
    """present a dict as an object which attributes are the keys"""
    def __init__(self, d):
        self.__d = d

    def __getattr__(self, a):
        try:
            return self.__d[a]
        except KeyError:
            raise AttributeError('no such key in dict: %s' % a)


class Counter(object):
    """self incrementing counter"""
    def __init__(self, start=0, inc=1, wrap=None):
        self.start = start
        self.val = start
        self.inc = inc
        self.wrap = wrap

    def __call__(self):
        v = self.val
        self.val += self.inc
        if self.wrap is not None and self.val >= self.wrap:
            self.val = self.start
        return v

    def __int__(self):
        return int(self.__call__())

    def __float__(self):
        return float(self.__call__())


class Switcher(object):
    """will switch between two results with every call"""
    def __init__(self, v=0, v0=0, v1=1):
        self.v = v
        self.v0 = v0
        self.v1 = v1

    def __call__(self):
        r = self.v and self.v1 or self.v0
        self.v = not self.v
        return r


class CallMultiplexer(object):
    """a multiplexer for function calls, dispatch a single call to
    more than one function"""
    def __init__(self, *f):
        self.flist = f

    def add(self, *f):
        self.flist = self.flist + f

    def __call__(self, *args, **kwargs):
        [f(*args, **kwargs) for f in self.flist]


### Files & friends

class FileMonitor(object):
    """monitors access and changes to a file"""

    def __init__(self, fname):
        self.name = fname
        self.lastACheck = time.time()
        self.lastMCheck = self.lastACheck

    def wasModified(self, ref=None):
        if not ref: ref=self.lastMCheck
        self.lastMCheck = time.time()
        return os.stat(self.name)[stat.ST_MTIME] > ref

    def wasAccessed(self, ref=None):
        if not ref: ref=self.lastACheck
        self.lastACheck = time.time()
        return os.stat(self.name)[stat.ST_ATIME] > ref


class FifoWriter(object):

    def __init__(self, fName, blocking=None, waittime=0.01):
        if not os.path.exists(fName):
            os.mkfifo(fName)
        self.fifo = open(fName, 'w')
        self.blocking = blocking
        self.waittime = waittime

    def check(self):
        return not len(select.select([], [self.fifo], [], 0)[1]) == 0

    def put(self, txt):
        if self.blocking:
            while not self.check():
                time.sleep(self.waittime)
        self.fifo.write(txt+'\n')
        self.fifo.flush()

    def close(self):
        self.fifo.close()


class FifoReader(object):

    def __init__(self, fName):
        if not os.path.exists(fName):
            os.mkfifo(fName)
        self.fifo = open(fName, 'r')

    def check(self):
        return not len(select.select([self.fifo], [], [], 0)[0]) == 0

    def get(self):
        if self.check():
            return self.fifo.readline()
        else:
            return None

    def close(self):
        self.fifo.close()


class FifoReaderMem(object):

    def __init__(self, fName):
        if not os.path.exists(fName):
            os.mkfifo(fName)
        self.fifo = open(fName, 'r')
        self.last = ""

    def check(self):
        return not len(select.select([self.fifo], [], [], 0)[0]) == 0

    def get(self):
        if self.check():
            self.last = self.fifo.readline()
            return self.last
        else:
            return self.last

    def close(self):
        self.fifo.close()

