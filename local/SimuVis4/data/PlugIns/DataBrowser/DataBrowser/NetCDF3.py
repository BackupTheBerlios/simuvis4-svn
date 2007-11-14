# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import os
from PyQt4.QtGui import QWidget, QTreeView, QAbstractItemView, QStandardItemModel, QStandardItem, \
    QVBoxLayout, QSplitter, QTextBrowser, QMessageBox
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt, SIGNAL, QCoreApplication

from pycdf import CDF, NC
from weakref import ref, proxy


class NetCDF3Browser(QWidget):
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
        self.model = NetCDF3Model()
        self.treeView.setModel(self.model)
        self.treeView.setSortingEnabled(True)
        self.treeView.expandAll()
        self.connect(self.treeView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.showItem)
        self.connect(self.treeView, SIGNAL("doubleClicked(QModelIndex)"), self.itemAction)

    def showItem(self, mi, pr):
        i = self.model.itemFromIndex(mi)
        nc = i.ncItem
        self.textBrowser.setText("<i>%s</i><br><b>%s: </b>%s" % (str(type(nc))[1:-1], i.data().toString(), nc))

    def itemAction(self, mi,):
        i = self.model.itemFromIndex(mi)
        nc = i.ncItem
        QMessageBox.information(self,
                QCoreApplication.translate('NetCDF3', 'netCDF3: Item clicked'),
                QCoreApplication.translate('NetCDF3', 'You clicked an item in the netCDF3-browser'))


class NetCDF3Model(QStandardItemModel):
    """simple model for netCDF Files"""

    def __init__(self):
        QStandardItemModel.__init__(self)
        self.rootItem = self.invisibleRootItem()
        self.setHorizontalHeaderLabels(['Element'])
        self.files = {}

    def addNcFile(self, ncFileName):
        f = CDF(ncFileName, NC.WRITE | NC.CREATE)
        self.files[ncFileName] = f
        fItem = QStandardItem(ncFileName)
        fItem.setData(QVariant(ncFileName))
        fItem.ncItem = f # proxy(f)
        self.rootItem.appendRow(fItem)
        for an,av in f.attributes().items():
            aItem = QStandardItem(an)
            aItem.setData(QVariant(an))
            aItem.ncItem = av
            fItem.appendRow(aItem)
        for vn in f.variables().keys():
            vItem = QStandardItem(vn)
            vItem.setData(QVariant(vn))
            vv = f.var(vn)
            vItem.ncItem = vv
            fItem.appendRow(vItem)
            for an,av in vv.attributes().items():
                aItem = QStandardItem(an)
                aItem.setData(QVariant(an))
                aItem.ncItem = av
                vItem.appendRow(aItem)
