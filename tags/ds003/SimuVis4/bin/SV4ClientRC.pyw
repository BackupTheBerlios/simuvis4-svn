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
        code = unicode(self.codeInput.toPlainText())
        host = str(self.hostInput.text())
        port = int(self.portInput.value())
        sendCode(code, host, port)


def sendCode(code, host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(code)
        s.close()
        return True
    except:
        # FIXME: some error handling
        return False


if __name__ == "__main__":
    import sys, os, getopt, string
    host = '127.0.0.1'
    port = 12345
    gui = True
    app = os.path.split(sys.argv[0])[-1]
    help = string.Template("""
Usage: $app [options] [<scriptfiles>]
Options include:
    -h
    --help
        print this help and exit
    -t hostname_or_ip
    --target=hostname_or_ip
        send to hostname or ip, default is (127.0.0.1) localhost
    -p portnumber
    --port=portnumber
        use target portnumber, default is $defPort
    -n
    --nowin
        send code immediately without showing a GUI window,
        if no scriptfile is given stdin is read

<scriptfiles> means one or more python files

Examples:
    $app -n -p 23456 foo.py
        send contents of foo.py to localhost, port 23456 immediately

    $app --target=otherhost foo.py bar.py
        send contents of foo.py and bar.py to otherhost, port $defPort using the GUI

    someCommand | $app -n
        send the output of someCommand immediately to localhost, port $defPort
""").substitute(app=app, defPort=port)
    sopt = 'ht:p:n'
    lopt  = ['help', 'target=', 'port=', 'nowin']
    if not ('-n' in sys.argv or '--nowin' in sys.argv):
        # let Qt delete its specific options first
        app = QtGui.QApplication(sys.argv)
    else:
        gui = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], sopt, lopt)
    except getopt.GetoptError:
        print help
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            print help
            sys.exit(0)
        if o in ('-t', '--target'):
            host = a
        if o in ('-p', '--port'):
            port = int(a)
        if o in ('-n', '--nowin'):
            gui = False # should alraedy be set
    if args:
        code = os.linesep.join([open(f, 'r').read() for f in args])
    else:
        if not gui:
            code = sys.stdin.read()
        else:
            code = "# Please enter code here!" + os.linesep
    if not code:
        print 'Not sending empty script, use -h or --help for help!'
        sys.exit(3)

    if gui:
        mainWidget = SV4RemoteClientUI()
        mainWidget.codeInput.setText(code)
        mainWidget.hostInput.setText(host)
        mainWidget.portInput.setValue(port)
        mainWidget.show()
        sys.exit(app.exec_())
    else:
        sys.exit(not sendCode(code, host, port))
