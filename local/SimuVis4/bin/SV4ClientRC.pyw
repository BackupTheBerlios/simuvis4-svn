#!/usr/bin/python 
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import socket

class SV4RemoteClientUI(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setObjectName("self")
        self.resize(QtCore.QSize(QtCore.QRect(0,0,471,238).size()).expandedTo(self.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(self)
        self.vboxlayout.setObjectName("vboxlayout")

        self.codeInput = QtGui.QTextEdit(self)
        self.codeInput.setObjectName("codeInput")
        self.codeInput.setText("# enter remote code here")
        self.vboxlayout.addWidget(self.codeInput)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.hostLabel = QtGui.QLabel(self)
        self.hostLabel.setObjectName("hostLabel")
        self.hboxlayout.addWidget(self.hostLabel)

        self.hostInput = QtGui.QLineEdit(self)
        self.hostInput.setObjectName("hostInput")
        self.hostInput.setText('127.0.0.1')
        self.hboxlayout.addWidget(self.hostInput)

        self.portLabel = QtGui.QLabel(self)
        self.portLabel.setObjectName("portLabel")
        self.hboxlayout.addWidget(self.portLabel)

        self.portInput = QtGui.QSpinBox(self)
        self.portInput.setMaximum(500000)
        self.portInput.setValue(12345)
        self.portInput.setObjectName("portInput")
        self.hboxlayout.addWidget(self.portInput)

        self.sendButton = QtGui.QPushButton(self)
        self.sendButton.setObjectName("sendButton")
        self.hboxlayout.addWidget(self.sendButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi()
        self.connect(self.sendButton, QtCore.SIGNAL("pressed()"), self.run)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("SV4ClientRC", "SV4 Client for RemoteControl", None, QtGui.QApplication.UnicodeUTF8))
        self.hostLabel.setText(QtGui.QApplication.translate("SV4ClientRC", "Host:", None, QtGui.QApplication.UnicodeUTF8))
        self.portLabel.setText(QtGui.QApplication.translate("SV4ClientRC", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("SV4ClientRC", "Send", None, QtGui.QApplication.UnicodeUTF8))

    def run(self):
        code = str(self.codeInput.toPlainText())
        host = str(self.hostInput.text())
        port = int(self.portInput.value())
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(code)
            s.close()
        except SocketError:
            # FIXME: some error handling
            pass

if __name__ == "__main__":
    import sys, os
    app = QtGui.QApplication(sys.argv)
    mainWidget = SV4RemoteClientUI()
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[-1]):
        mainWidget.codeInput.setText(open(sys.argv[-1], 'r').read())
    mainWidget.show()
    sys.exit(app.exec_())
