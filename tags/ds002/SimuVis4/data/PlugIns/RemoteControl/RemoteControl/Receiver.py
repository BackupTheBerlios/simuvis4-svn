# encoding: utf-8
# version:  $Id: PyConsoleWindow.py 66 2007-11-17 18:24:26Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, sys
from PyQt4.QtCore import QTimer, QCoreApplication, QObject, SIGNAL
#from PyQt4.QtGui import QMessageBox
from PyQt4.QtNetwork import QTcpServer, QTcpSocket, QHostAddress


class CodeReceiver(QTcpServer):

    def __init__(self, port, ipFilter='', raiseOnExec=False, raiseHack=False):
        QTcpServer.__init__(self)
        self.enabled = False
        self.ipFilter = ipFilter
        self.raiseOnExec = raiseOnExec
        self.raiseHack = raiseHack
        self.counter = SimuVis4.Misc.Counter()
        self.listen(QHostAddress(QHostAddress.LocalHost), port)


    def setEnabled(self, e):
        self.enabled = e


    def incomingConnection(self, socket):
        if not self.enabled:
            return
        s = QTcpSocket(self)
        s.setSocketDescriptor(socket)
        sIp = unicode(s.peerAddress().toString())
        sPort = s.peerPort()
        if sIp.startswith(self.ipFilter):
            SimuVis4.Globals.logger.info(unicode(QCoreApplication.translate('RemoteControl',
                'RemoteControl: accepting connection from %s, port %s')), sIp, sPort)
            self.connect(s, SIGNAL('readyRead()'), self.readClient)
            self.connect(s, SIGNAL('disconnected()'), self.discardClient)
        else:
            SimuVis4.Globals.logger.error(unicode(QCoreApplication.translate('RemoteControl',
                'RemoteControl: refusing connection from %s, port %s')), sIp, sPort)
            self.discardClient()


    def discardClient(self):
        socket = self.sender()
        socket.deleteLater()


    def readClient(self):
        if not self.enabled:
            return
        s = self.sender()
        d = s.readAll()
        s.close()
        if s.state() == QTcpSocket.UnconnectedState:
            del s
        self.executeCode(d)


    def executeCode(self, d):
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

