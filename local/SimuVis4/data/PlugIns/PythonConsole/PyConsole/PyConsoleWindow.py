# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import sys
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import SIGNAL, QCoreApplication
from SimuVis4.SubWin import SubWindow
from QPyShell import QPyShell


class PyConsoleWindow(SubWindow):

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('PyConsoleWindow', 'Python console'))
        self.console = QPyShell(self)
        self.mainLayout.addWidget(self.console)
        #self.setFocusProxy(self.console)
        self.setMinimumSize(600, 400)
        self.toggleVisibleAction.setText(QCoreApplication.translate('PyConsoleWindow', 'Python console'))
        self.toggleVisibleAction.setShortcut(QCoreApplication.translate('PyConsoleWindow', "Ctrl+D"))
        self.toggleVisibleAction.setStatusTip(QCoreApplication.translate('PyConsoleWindow', 'Python console'))

    def printWindow(self, printer=None):
        self.console.printContents(printer)

    def saveWindow(self, fileName=None):
        self.console.saveContents(fileName)
