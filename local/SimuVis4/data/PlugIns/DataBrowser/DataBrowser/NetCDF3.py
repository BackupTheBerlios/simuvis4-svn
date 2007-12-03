# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os
from PyQt4.QtGui import QWidget, QTreeView, QAbstractItemView, QStandardItemModel, QStandardItem, \
    QVBoxLayout, QHBoxLayout, QSplitter, QTextBrowser, QMessageBox, QToolButton, QIcon, QPixmap, \
    QFrame, QFileDialog
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt, SIGNAL, QCoreApplication

try:
    from Scientific.IO.NetCDF import NetCDFFile
except ImportError:
    SimuVis4.Globals.logger.warning(str(QCoreApplication.translate('DataBrowser',
        'Scientific.IO.NetCDF not found, trying to use pupynere instead')))
    from pupynere import NetCDFFile


class NetCDF3Browser(QWidget):
    """netCDF-Browser"""

    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)

        self.toolBar = QFrame(self)
        self.toolBarLayout = QHBoxLayout(self.toolBar)
        self.toolBarLayout.setMargin(2)
        self.toolBarLayout.setSpacing(2)
        self.layout.addWidget(self.toolBar)

        self.loadButton = QToolButton(self.toolBar)
        self.loadButton.setText(QCoreApplication.translate('NetCDF3', 'Open...'))
        self.loadButton.setIcon(QIcon(QPixmap(SimuVis4.Icons.fileOpen)))
        self.loadButton.setToolTip(QCoreApplication.translate('NetCDF3', 'Open a netCDF3 file'))
        self.toolBarLayout.addWidget(self.loadButton)
        self.connect(self.loadButton, SIGNAL('pressed()'), self.loadFile)

        self.dropButton = QToolButton(self.toolBar)
        self.dropButton.setText(QCoreApplication.translate('NetCDF3', 'Close All'))
        self.dropButton.setIcon(QIcon(QPixmap(SimuVis4.Icons.clear)))
        self.dropButton.setToolTip(QCoreApplication.translate('NetCDF3', 'Drop all open netCDF3 files'))
        self.toolBarLayout.addWidget(self.dropButton)
        self.connect(self.dropButton, SIGNAL('pressed()'), self.dropFiles)
        self.dropButton.setEnabled(False)

        self.toolBarLayout.addStretch(100)

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.treeView = QTreeView(self.splitter)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.textBrowser = QTextBrowser(self.splitter)
        self.layout.addWidget(self.splitter)
        self.splitter.setStretchFactor(0, 90)
        self.splitter.setStretchFactor(1, 10)
        self.model = NetCDF3Model()
        self.treeView.setModel(self.model)
        self.treeView.setSortingEnabled(True)
        self.treeView.expandAll()
        self.connect(self.treeView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.showItem)
        self.connect(self.treeView, SIGNAL("doubleClicked(QModelIndex)"), self.itemAction)

    def loadFile(self, fn=None):
        if not fn:
            fn = QFileDialog.getOpenFileName(self, QCoreApplication.translate('NetCDF3', "Select netCDF3 file to open"),
                SimuVis4.Globals.defaultFolder)
            if not fn.isEmpty():
                fn = unicode(fn)
                SimuVis4.Globals.defaultFolder, tmp = os.path.split(fn)
            else:
                return
        self.model.addNcFile(fn)

    def dropFiles(self):
        # FIXME: ...
        pass

    def itemAction(self, mi,):
        # FIXME: use a MIME-Handler here
        i = self.model.itemFromIndex(mi)
        t, nc = i.ncItem
        QMessageBox.information(self,
                QCoreApplication.translate('NetCDF3', 'netCDF3: Item clicked'),
                QCoreApplication.translate('NetCDF3', 'You clicked an item in the netCDF3-browser'))

    def showItem(self, mi, pr):
        i = self.model.itemFromIndex(mi)
        t, nc = i.ncItem
        txt = ""
        name = str(i.data().toString())
        if t == 'F':
            p, f = os.path.split(name)
            txt = "<i>File </i><b>%s</b><br> in %s" % (f, p)
        elif t == 'A':
            txt = "<i>Attribute </i><b>%s:</b><br>%s" % (name, unicode(nc))
        elif t == 'D':
            txt = "<i>Dimension </i><b>%s:</b><br>%s" % (name, str(nc))
        elif t == 'V':
            txt = "<i>Variable </i><b>%s:</b><br>Typecode: %s<br>Dimensions: %s<br>Shape: %s" % \
                (name, nc.typecode(), '*'.join(d for d in nc.dimensions), nc.shape)
        else:
            return
        self.textBrowser.setText(txt)


class NetCDF3Model(QStandardItemModel):
    """simple model for netCDF Files"""

    def __init__(self):
        QStandardItemModel.__init__(self)
        self.rootItem = self.invisibleRootItem()
        self.setHorizontalHeaderLabels(['Element'])
        self.files = {}
        import Icons
        self.icons = {
            'file' : QIcon(QPixmap(Icons.ncFile)),
            'variable' : QIcon(QPixmap(Icons.ncVar)),
            'dimension' : QIcon(QPixmap(Icons.ncDim)),
            'attribute' : QIcon(QPixmap(Icons.ncAtt))
        }

    def addNcFile(self, ncFileName):
        f = NetCDFFile(ncFileName) 
        self.files[ncFileName] = f
        fItem = QStandardItem(ncFileName)
        fItem.setIcon(self.icons['file'])
        fItem.setData(QVariant(ncFileName))
        fItem.ncItem = ('F', f)
        self.rootItem.appendRow(fItem)
        for an,av in ncFAttributes(f).items():
            aItem = QStandardItem(an)
            aItem.setIcon(self.icons['attribute'])
            aItem.setData(QVariant(an))
            aItem.ncItem = ('A', av)
            fItem.appendRow(aItem)
        for dn,dv in f.dimensions.items():
            dItem = QStandardItem(dn)
            dItem.setIcon(self.icons['dimension'])
            dItem.setData(QVariant(dn))
            dItem.ncItem = ('D', dv)
            fItem.appendRow(dItem)
        for vn, vv in f.variables.items():
            vItem = QStandardItem(vn)
            vItem.setIcon(self.icons['variable'])
            vItem.setData(QVariant(vn))
            vItem.ncItem = ('V', vv)
            fItem.appendRow(vItem)
            for an,av in ncVAttributes(vv).items():
                aItem = QStandardItem(an)
                aItem.setIcon(self.icons['attribute'])
                aItem.setData(QVariant(an))
                aItem.ncItem = ('A', av)
                vItem.appendRow(aItem)


_fSkipNames = ('close', 'flush', 'sync', 'createDimension', 'createVariable')
def ncFAttributes(f):
    """return a dictionary globals attributes"""
    if hasattr(f, 'attributes'):
        # seems to be a pupynere NetCDFFile
        return f.attributes
    d = {}
    for a in dir(f):
        if not a in _fSkipNames:
            d[a] = getattr(f, a)
    return d


_vSkipNames = ('assignValue', 'getValue', 'typecode')
def ncVAttributes(v):
    """return a dictionary of attributes of a variable"""
    if hasattr(v, 'attributes'):
        # seems to be a pupynere NetCDFVariable
        return f.attributes
    d = {}
    for a in dir(v):
        if not a in _vSkipNames:
            d[a] = getattr(v, a)
    return d
