# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os
from PyQt4.QtGui import QDockWidget, QToolBox, QLabel, QTreeView, QDirModel, QFrame, QVBoxLayout, QDesktopServices, \
    QAbstractItemView, QMenu
from PyQt4.QtCore import Qt, SIGNAL, QCoreApplication, QUrl


class Browser(QDockWidget):
    """abstract browser container based on a QToolBox,
    may contain different real browser implementations"""
    def __init__(self):
        QDockWidget.__init__(self, QCoreApplication.translate('DataBrowser', "Data Browser"))
        self.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetVerticalTitleBar)
        self.setMinimumSize(350, 500)
        self.toolBox = QToolBox(self)
        self.setWidget(self.toolBox)


class FileSystemBrowser(QTreeView):
    """simple file system browser"""

    def __init__(self):
        QTreeView.__init__(self)
        self.model = QDirModel()
        self.setModel(self.model)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setAutoExpandDelay(500)
        i = self.model.index(os.getcwd())
        self.scrollTo(i)
        self.expand(i)
        self.setCurrentIndex(i)
        for i in range(self.model.columnCount()):
            self.resizeColumnToContents(i)
        self.connect(self, SIGNAL("doubleClicked(QModelIndex)"), self.itemAction)
        self.connect(self, SIGNAL("customContextMenuRequested(QPoint)"), self.showContextMenu)


    def itemAction(self, mi):
        """default action (on doubleclick) for item at model index mi"""
        fi = self.model.fileInfo(mi)
        if self.model.isDir(mi):
            return
        self.filePath = str(fi.absoluteFilePath())
        if not SimuVis4.Globals.fileTypeActions.openFile(self.filePath):
            self.openExternal()

    def showContextMenu(self, pos):
        """show context menu for item at pos"""
        mi = self.indexAt(pos)
        fi = self.model.fileInfo(mi)
        if self.model.isDir(mi):
            return
        self.filePath = str(fi.absoluteFilePath())
        m = QMenu()
        for a in SimuVis4.Globals.fileTypeActions.getActions(self.filePath):
            # this is weird, ... but it works
            m.addAction(a[0], lambda b=a[1]: b(self.filePath))
        m.addSeparator()
        m.addAction(QCoreApplication.translate('DataBrowser', 'Open external'),
            self.openExternal)
        a = m.exec_(self.mapToGlobal(pos))

    def openExternal(self, filePath=None):
        if not filePath:
            filePath = self.filePath
        QDesktopServices.openUrl(QUrl.fromLocalFile(filePath))
        #os.startfile(filePath) # only under windows... ?
