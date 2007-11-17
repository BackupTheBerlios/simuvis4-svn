# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework


"""Executor - execute python code in separate threads"""

from PyQt4.QtGui import QProgressDialog
from PyQt4.QtCore import SIGNAL, QCoreApplication

import os, threading, sys
import Misc, Globals

logger = Globals.logger

globalNameSpace = Globals.__dict__ # gobals()

def _execute(s):
    exec s in globalNameSpace
    

class Executor(object):
    
    def __init__(self):
        self._threads = {}
        self._cnt = Misc.Counter()
        self.cancelFlag = False

    def preRun(self, name):
        pass

    def postRun(self, name):
        pass

    def progress(self, i):
        pass

    def cancel(self):
        self.cancelFlag = True

    def run(self, c, name=None):
        if not name:
            name = 'code_%d' % self._cnt()
        logger.info(unicode(QCoreApplication.translate('Executor', 'Executor: running code "%s"')), name)
        self.preRun(name)
        try:
            _execute(c)
        finally:
            self.postRun(name)
            self.cancelFlag = False
        
    def runFile(self, f, name=None):
        """run python code from file-like object f"""
        return self.run(f.read(), name)

    def runFilename(self, name):
        """run python code from file with name n"""
        return self.run(open(name, 'r').read(), name)
    
    def thread(self, c, name=None):
        """run python code c in a separate thread with name name"""
        if not name:
            name = 'thread_%d' % self._cnt()
        if name in self.threads and self.threads[n].isAlive():
                raise NameError(unicode(QCoreApplication.translate('Executor', 'thread with this name is still running')))
        logger.info(unicode(QCoreApplication.translate('Executor', 'Executor: running code in thread "%s"')), name)
        thread = threading.Thread(name=name, target=_execute, args=(c,))
        self._threads[name] = thread
        thread.start()
        return name

    def threadFile(self, f, name=None):
        """run python code from file-like object f"""
        return self.thread(f.read(), name)

    def threadFilename(self, name):
        """run python code from file with name n"""
        return self.thread(open(name, 'r').read(), name)

    def waitForThread(self, name, timeout=None):
        """wait for execution thread n to finish, but wait at most
        timeout seconds. return true if thread is finished and false
        if it is still alive"""
        thread = self.threads[name]
        thread.join(timeout)
        return not thread.isAlive()
                
    def cleanThreads(self):
        """forget all finished threads, return number of active threads"""
        for name, thread in self.threads.items():
            if not thread.isAlive():
                del self.threads[name]
        l = len(self.threads)
        logger.debug(unicode(QCoreApplication.translate('Executor', 'Executor: cleaned up ... %d threads running')), l)
        return l


class ExecutorQt(Executor):
    def preRun(self, name):
        if not hasattr(self, 'dlg'):
            self.dlg = QProgressDialog(Globals.mainWin)
            self.dlg.setWindowTitle(QCoreApplication.translate('Executor', 'Execution progress'))
            self.dlg.connect(self.dlg, SIGNAL("canceled()"), self.cancel)
        self.dlg.show()
        self.dlg.setValue(0)

    def postRun(self, name):
        self.dlg.setValue(100)
        self.dlg.hide()

    def progress(self, i):
        self.dlg.setValue(i)
        if Globals.application.hasPendingEvents():
                Globals.application.processEvents()
