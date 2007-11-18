# encoding: utf-8
# version:  $Id: VtkWindow.py 67 2007-11-17 18:25:01Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from SimuVis4.SubWin import SubWindow
from PyQt4.Qwt5 import QwtPlot
from PyQt4.QtGui import QFrame, QHBoxLayout, QToolButton, QSizePolicy
from PyQt4.QtCore import SIGNAL, QCoreApplication

class QwtPlotWindow(SubWindow):
    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('QwtPlot', 'QwtPlotWindow'))
        self.plotWidget = QwtPlot(self)
        self.mainLayout.setMargin(0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.plotWidget, 1)
        self.setFocusProxy(self.plotWidget)
        self.resize(100, 100)
        self.setMinimumSize(200, 200)
        self.toolBar = None

    def makeToolBar(self):
        #FIXME: this is just a placeholder
        if self.toolBar:
            return
        self.toolBar = QFrame(self)
        self.toolBarLayout = QHBoxLayout(self.toolBar)
        self.toolBarLayout.setMargin(0)
        self.toolBarLayout.setSpacing(0)

        self.fooButton = QToolButton(self.toolBar)
        self.fooButton.setText('Foo')
        self.toolBarLayout.addWidget(self.fooButton)
    
        self.mainLayout.addWidget(self.toolBar, 0)
        self.toolBar.show()