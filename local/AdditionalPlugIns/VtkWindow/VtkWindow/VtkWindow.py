# encoding: latin-1
# version:  $Id: VtkWindow.py,v 1.5 2007/04/21 17:32:47 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from SimuVis4.SubWin import SubWindow
from VtkWidget import VtkWidget
from PyQt4.QtGui import QFrame, QHBoxLayout, QToolButton, QSizePolicy
from PyQt4.QtCore import SIGNAL, QCoreApplication

class VtkWindow(SubWindow):
    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('VtkWindow', 'VtkWindow'))
        self.vtkWidget = VtkWidget(parent=self)
        self.mainLayout.setMargin(0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.vtkWidget, 1)
        self.setFocusProxy(self.vtkWidget)
        self.resize(100, 100)
        self.setMinimumSize(200, 200)
        self.toolBar = None

    def makeToolBar(self):
        # FIXME: mor actions, connects ...
        if self.toolBar:
            return
        self.toolBar = QFrame(self)
        self.toolBarLayout = QHBoxLayout(self.toolBar)
        self.toolBarLayout.setMargin(0)
        self.toolBarLayout.setSpacing(0)

        self.xViewButton = QToolButton(self.toolBar)
        self.xViewButton.setText('|X|')
        self.toolBarLayout.addWidget(self.xViewButton)

        self.yViewButton = QToolButton(self.toolBar)
        self.yViewButton.setText('|Y|')
        self.toolBarLayout.addWidget(self.yViewButton)

        self.zViewButton = QToolButton(self.toolBar)
        self.zViewButton.setText('|Z|')
        self.toolBarLayout.addWidget(self.zViewButton)

        self.toolBarLayout.addStretch(1)

        self.mainLayout.addWidget(self.toolBar, 0)
        self.toolBar.show()