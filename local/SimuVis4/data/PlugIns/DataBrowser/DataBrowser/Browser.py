# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import os
from PyQt4.QtGui import QDockWidget, QToolBox, QLabel, QTreeView, QDirModel, QFrame, QVBoxLayout
from PyQt4.QtCore import SIGNAL, QCoreApplication


class Browser(QDockWidget):
    """abstract browser container based on a QToolBox,
    may contain different real browser implementations"""
    def __init__(self):
        QDockWidget.__init__(self, QCoreApplication.translate('DataBrowser', "Data Browser"))
        self.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetVerticalTitleBar)
        self.setMinimumSize(350, 500)
        self.frame = QFrame(self)
        #self.frame.setFrameStyle(QFrame.Panel)
        self.setWidget(self.frame)
        self.frameLayout = QVBoxLayout(self.frame)
        self.frameLayout.setMargin(0)
        self.frameLayout.setSpacing(0)
        self.toolBox = QToolBox(self.frame)
        self.frameLayout.addWidget(self.toolBox, 1)


class FileSystemBrowser(QTreeView):
    """simple file system browser, no actions yet"""

    def __init__(self):
        QTreeView.__init__(self)
        self.model = QDirModel()
        self.setModel(self.model)
        self.setSortingEnabled(True)
        i = self.model.index(os.getcwd())
        self.scrollTo(i)
        self.expand(i)
        self.setCurrentIndex(i)
        for i in range(self.model.columnCount()):
            self.resizeColumnToContents(i)
