# encoding: utf-8
# version:  $Id: PyConsoleWindow.py 66 2007-11-17 18:24:26Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, sys, socket, threading, Queue, time
from PyQt4.QtCore import QTimer, QCoreApplication, QObject, SIGNAL
from PyQt4.QtGui import QMessageBox

shutdownEvent = threading.Event()

def listen_tcp(port, queue, ipFilter):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.settimeout(1.0)
    except:
        SimuVis4.Globals.logger.exception(unicode(QCoreApplication.translate('RemoteControl',
            'RemoteControl: could not start TCP listener at port %s')), port)
        return
    while not shutdownEvent.isSet():
        data = []
        try:
            s.listen(1)
            conn, addr = s.accept()
            conn.setblocking(True)
            sip, sport = addr
            if sip.startswith(ipFilter):
                SimuVis4.Globals.logger.info(unicode(QCoreApplication.translate('RemoteControl',
                    'RemoteControl: accepting connection from %s, port %d')), sip, sport)
                while 1:
                    d = conn.recv(4096)
                    if not d: break
                    data.append(d)
                queue.put(''.join(data), True)
                conn.close()
            else:
                SimuVis4.Globals.logger.error(unicode(QCoreApplication.translate('RemoteControl',
                    'RemoteControl: refusing connection from %s, port %d')), sip, sport)
        except socket.timeout:
            pass
    s.close()


class CodeReceiver:

    def __init__(self, tcpPort, qSize, ipFilter='', raiseOnExec=False, raiseHack=False):
        self.queue = Queue.Queue(qSize)
        self.counter = SimuVis4.Misc.Counter()
        SimuVis4.Globals.logger.info(unicode(QCoreApplication.translate('RemoteControl',
            'RemoteControl: starting thread for TCP listener at port %s')), tcpPort)
        self.tcpListener = threading.Thread(target=listen_tcp, args=(tcpPort, self.queue, ipFilter))
        self.tcpListener.start()
        self.raiseOnExec = raiseOnExec
        self.raiseHack = raiseHack
        self.timer = QTimer(SimuVis4.Globals.mainWin)
        QObject.connect(self.timer, SIGNAL('timeout()'), self.execute)

    def setEnabled(self, e=True):
        if e:
            self.timer.start(100)
        else:
            if self.timer.isActive():
                self.timer.stop()

    def shutdown(self):
        shutdownEvent.set()
        self.tcpListener.join(3)
        if self.tcpListener.isAlive():
            QMessageBox.critical(SimuVis4.Global.mainWin,
                QCoreApplication.translate('RemoteControl', 'RemoteControl: Could not stop receiver!'),
                QCoreApplication.translate('RemoteControl', 'Stopping the receiver thread of the RemoteContol plugin failed!'))

    def execute(self):
        if self.queue.empty():
            return
        else:
            d = self.queue.get(5.0, True)
            SimuVis4.Globals.logger.debug(unicode(QCoreApplication.translate('RemoteControl',
                'RemoteControl: trying to run code:')))
            SimuVis4.Globals.logger.debug('-'*60)
            SimuVis4.Globals.logger.debug(unicode(d))
            SimuVis4.Globals.logger.debug('-'*60)
            name = "Remote Code %d" % self.counter()
            if self.raiseOnExec:
                if self.raiseHack:
                    SimuVis4.Globals.mainWin.hide()
                    SimuVis4.Globals.mainWin.show()
                else:
                    SimuVis4.Globals.mainWin.raise_()
            SimuVis4.Globals.mainWin.executor.run(d, name=name)

    def __del__(self):
        self.shutdown()
