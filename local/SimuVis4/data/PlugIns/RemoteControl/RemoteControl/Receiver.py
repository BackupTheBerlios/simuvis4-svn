# encoding: utf-8
# version:  $Id: PyConsoleWindow.py 66 2007-11-17 18:24:26Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, sys, socket, threading, Queue
from PyQt4.QtCore import QTimer, QCoreApplication, QObject, SIGNAL


def listen_tcp(port, queue, ipFilter):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    while 1:
        data = []
        s.listen(1)
        conn, addr = s.accept()
        sip, sport = addr
        if sip.startswith(ipFilter):
            SimuVis4.Globals.logger.info(unicode(QCoreApplication.translate('RemoteControl',
                'RemoteControl: accepting connection from %s, port %d')), sip, sport)
            while 1:
                d = conn.recv(1024)
                if not d: break
                data.append(d)
            queue.put(''.join(data), True)
            conn.close()
        else:
            SimuVis4.Globals.logger.warning(unicode(QCoreApplication.translate('RemoteControl',
                'RemoteControl: refusing connection from %s, port %d')), sip, sport)


class CodeReceiver:

    def __init__(self, tcpPort, qSize, ipFilter=''):
        self.queue = Queue.Queue(qSize)
        self.counter = SimuVis4.Misc.Counter()
        SimuVis4.Globals.logger.info(unicode(QCoreApplication.translate('RemoteControl',
            'RemoteControl: starting TCP listener at port %d'), tcpPort))
        self.tcpListener = threading.Thread(target=listen_tcp, args=(tcpPort, self.queue, ipFilter))
        self.timer = QTimer(SimuVis4.Globals.mainWin)
        QObject.connect(self.timer, SIGNAL('timeout()'), self.execute)

    def setEnabled(self, e=True):
        if e:
            if self.tcpListener and not self.tcpListener.isAlive():
                self.tcpListener.start()
            self.timer.start(100)
        else:
            if self.timer.isActive():
                self.timer.stop()

    def shutdown(self):
        self.timer.stop()
        # FIXME: close threads

    def execute(self):
        if self.queue.empty():
            return
        else:
            d = self.queue.get(5.0, True)
            SimuVis4.Globals.logger.debug(unicode(QCoreApplication.translate('RemoteControl', 'RemoteControl: trying to run code:')))
            SimuVis4.Globals.logger.debug('-'*60)
            SimuVis4.Globals.logger.debug(unicode(d))
            SimuVis4.Globals.logger.debug('-'*60)
            name = "Remote Code %d" % self.counter()
            SimuVis4.Globals.mainWin.executor.run(d, name=name)
