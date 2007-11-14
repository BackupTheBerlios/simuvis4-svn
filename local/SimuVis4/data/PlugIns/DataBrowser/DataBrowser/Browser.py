# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import os
from PyQt4.QtGui import QDockWidget, QToolBox, QLabel, QTreeView, QDirModel, QFrame, QVBoxLayout
from PyQt4.QtCore import SIGNAL, QCoreApplication


class Browser(QDockWidget):
    """abstract browser based on a QToolBox, may contain different real browser implementations"""
    def __init__(self):
        QDockWidget.__init__(self, 'Data Browser')
        self.frame = QFrame(self)
        #self.frame.setFrameStyle(QFrame.Panel)
        self.setWidget(self.frame)
        self.frameLayout = QVBoxLayout(self.frame)
        self.frameLayout.setMargin(2)
        self.frameLayout.setSpacing(6)
        self.toolBox = QToolBox(self.frame)
        self.frameLayout.addWidget(self.toolBox, 1)


class FileSystemBrowser(QTreeView):
    """simple file system browser"""

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
