# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from SimuVis4.SubWin import SubWindow
from VtkWidget import VtkWidget
from PyQt4.QtGui import QFrame, QHBoxLayout, QToolButton, QSizePolicy, QMdiSubWindow
from PyQt4.QtCore import SIGNAL, QCoreApplication


class VtkWindow(SubWindow):
    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('VtkWindow', 'VtkWindow'))
        self.vtkWidget = VtkWidget(parent=self)
        self.setWidget(self.vtkWidget)
        self.setFocusProxy(self.vtkWidget)
        self.resize(100, 100)
        self.setMinimumSize(200, 200)
