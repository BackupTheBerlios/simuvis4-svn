# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import os
from PyQt4.QtGui import QWidget, QTreeView, QAbstractItemView, QStandardItemModel, QStandardItem, \
    QVBoxLayout, QSplitter, QTextBrowser, QMessageBox
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt, SIGNAL, QCoreApplication

from datastorage.database import DataBaseRoot, Sensor

class DSBrowser(QWidget):
    """netCDF-Browser"""

    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.treeView = QTreeView(self.splitter)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.textBrowser = QTextBrowser(self.splitter)
        self.layout.addWidget(self.splitter)
        self.splitter.setStretchFactor(0, 85)
        self.splitter.setStretchFactor(1, 15)
        self.model = DSModel()
        self.treeView.setModel(self.model)
        self.treeView.setSortingEnabled(True)
        self.treeView.expandAll()
        self.connect(self.treeView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.showItem)
        self.connect(self.treeView, SIGNAL("doubleClicked(QModelIndex)"), self.itemAction)


    def node(self, mi):
        item = self.model.itemFromIndex(mi)
        path = str(item.data().toString())
        return self.model.database.find(path)


    def showItem(self, mi, pr):
        n = self.node(mi)
        if isinstance(n, Sensor):
            txt = "<b>%s:</b><br>Start: %d<br>Stop: %d<br>Step: %d<br>Len: %d" % \
                (n.name, n.timegrid.start, n.timegrid.stop, n.timegrid.step, n.datalen())
            self.textBrowser.setText(txt)

    def itemAction(self, mi,):
        n = self.node(mi)
        if isinstance(n, Sensor):
            import PyQt4.Qwt5 as Qwt
            import SimuVis4
            sw = SimuVis4.SubWin.SubWindow(SimuVis4.Globals.mainWin.workSpace)
            sw.setWindowTitle(n.path)
            plt = Qwt.QwtPlot()
            sw.mainLayout.addWidget(plt)
            sw.setFocusProxy(plt)
            SimuVis4.Globals.mainWin.workSpace.addWindow(sw)
            curve = Qwt.QwtPlotCurve('data')
            curve.attach(plt)
            print type(n.data)
            print len(n.data)
            print n.data
            curve.setData(range(len(n.data)), list(n.data))
            sw.show()


class DSModel(QStandardItemModel):
    """simple model for netCDF Files"""

    def __init__(self):
        QStandardItemModel.__init__(self)
        self.rootItem = self.invisibleRootItem()
        self.setHorizontalHeaderLabels(['Element'])
        self.database = None

    def addDatabase(self, folder):
        db = DataBaseRoot(folder)
        self.database = db
        self.build(db, self.rootItem)

    def build(self, node, parent):
        for k, v in node.items():
            item = QStandardItem(k)
            item.setData(QVariant(v.path))
            parent.appendRow(item)
            self.build(v, item)
