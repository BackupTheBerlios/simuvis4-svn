# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""Misc - misc. general functions and classes"""

import os, time, stat, re, select, mimetypes



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



class RingBuffer(list):
    """list that behaves like a ring buffer,
    next() gives the next element, starting over
    when done"""

    def __init__(self, *arg, **kwarg):
        list.__init__(self, *arg, **kwarg)
        self._index = -1

    def next(self):
        if self._index < (len(self)-2):
            self._index += 1
        else:
            self._index = 0
        return self[self._index]

    def __call__(self):
        return self.next()



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



class BoolSignal(object):
    def __init__(self, vunset = False, vset = True):
        self._unset = vunset
        self._set = vset
        self._v = vunset

    def set(self):
        self._v = self._set

    def unset(self):
        self._v = self._unset

    def toggle(self):
        if self.isSet():
            self._v = self._unset
        else:
            self._v = self._set

    def isSet(self):
        return self._v == self._set

    def __call__(self):
        return self._v



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



def uniqueName(name, names, numFormat='%03d', sep='_'):
    """try to generate a unique name which is not already in names"""
    if not name in names:
        return name
    tmp = name.split(sep)
    try:
        tmp[-1] = numFormat % (int(tmp[-1])+1)
    except:
        tmp.append(numFormat % 0)
    name = sep.join(tmp)
    while name in names:
        tmp[-1] = numFormat % (int(tmp[-1])+1)
        name = sep.join(tmp)
    return name



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



def uniqueFileName(fileName, numFormat='%03d', sep='_'):
    """try to generate a unique, non-existent filename"""
    if not os.path.exists(fileName):
        return fileName
    base, ext = os.path.splitext(fileName)
    tmp = base.split(sep)
    try:
        tmp[-1] = numFormat % (int(tmp[-1])+1)
    except:
        tmp.append(numFormat % 0)
    fileName = sep.join(tmp) + ext
    while os.path.exists(fileName):
        tmp[-1] = numFormat % (int(tmp[-1])+1)
        fileName = sep.join(tmp) + ext
    return fileName


class FileActionRegistry:

    def __init__(self):
        self.actions = {}

    def addType(self, type, ext):
        mimetypes.add_type(type, ext)

    def addAction(self, action, types=[], name='', priority=1):
        for type in types:
            if not type in self.actions:
                self.actions[type] = [(name, action, priority)]
            else:
                self.actions[type].append((name, action, priority))
                self.actions[type].sort(lambda a, b: cmp(b[2], a[2]))

    def removeAction(self, action):
        pass # FIXME! implement function

    def fileType(self, fileName):
        return mimetypes.guess_type(fileName)[0]

    def hasActions(mimeType):
        return len(self.actions.get(mimeType, []))

    def openFile(self, fileName):
        tp = self.fileType(fileName)
        if not tp:
            return False
        for t in tp, tp.split('/')[0]:
            print t
            if t in self.actions:
                self.actions[t][0][1](fileName)
                return True
        return False

    def getActions(self, fileName):
        tp = self.fileType(fileName)
        if not tp:
            return []
        a = []
        for t in tp, tp.split('/')[0]:
            if t in self.actions:
                a += self.actions[t]
        return a
