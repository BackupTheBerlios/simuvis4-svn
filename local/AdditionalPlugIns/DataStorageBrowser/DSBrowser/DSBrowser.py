# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os, Icons
from PyQt4.QtGui import QWidget, QTreeView, QAbstractItemView, QStandardItemModel, QStandardItem, \
    QVBoxLayout, QHBoxLayout, QSplitter, QTextBrowser, QMessageBox, QToolButton, QIcon, QPixmap, \
    QFrame, QFileDialog
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt, SIGNAL, QCoreApplication

from datastorage.database import DataBaseRoot, Sensor


class DSBrowser(QWidget):
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
        self.loadButton.setText(QCoreApplication.translate('DataStorageBrowser', 'Open...'))
        self.loadButton.setIcon(QIcon(QPixmap(SimuVis4.Icons.fileOpen)))
        self.loadButton.setToolTip(QCoreApplication.translate('DataStorageBrowser', 'Open a datastorage database'))
        self.toolBarLayout.addWidget(self.loadButton)
        self.connect(self.loadButton, SIGNAL('pressed()'), self.loadDatabase)

        self.dropButton = QToolButton(self.toolBar)
        self.dropButton.setText(QCoreApplication.translate('DataStorageBrowser', 'Close All'))
        self.dropButton.setIcon(QIcon(QPixmap(SimuVis4.Icons.clear)))
        self.dropButton.setToolTip(QCoreApplication.translate('DataStorageBrowser', 'Drop all open databases'))
        self.toolBarLayout.addWidget(self.dropButton)
        self.connect(self.dropButton, SIGNAL('pressed()'), self.dropDatabases)
        self.dropButton.setEnabled(False)

        self.toolBarLayout.addStretch(100)

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


    def loadDatabase(self, dn=None):
        if not dn:
            dn = QFileDialog.getExistingDirectory(self, QCoreApplication.translate('DataStorageBrowser',
                "Select a folder containing a datastorage database"), SimuVis4.Globals.defaultFolder)
            if not dn.isEmpty():
                dn = unicode(dn)
                SimuVis4.Globals.defaultFolder = dn
            else:
                return
        self.model.addDatabase(dn)


    def dropDatabases(self):
        # FIXME: ...
        pass


    def node(self, mi):
        item = self.model.itemFromIndex(mi)
        p = str(item.data().toString())
        if '|' in p:
            db, path = p.split('|')
            return self.model.databases[db].find(path)
        else:
            return self.model.databases[p]


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
            SimuVis4.Globals.mainWin.workSpace.addSubWindow(sw)
            curve = Qwt.QwtPlotCurve('data')
            curve.attach(plt)
            print type(n.data)
            print len(n.data)
            print n.data
            curve.setData(range(len(n.data)), list(n.data))
            sw.show()


class DSModel(QStandardItemModel):
    """simple model for a datastorage database"""

    def __init__(self):
        QStandardItemModel.__init__(self)
        self.rootItem = self.invisibleRootItem()
        self.setHorizontalHeaderLabels(['Element'])
        self.databases = {}
        import Icons
        self.icons = {
            'database'    : QIcon(QPixmap(Icons.database)),
            'project'     : QIcon(QPixmap(Icons.project)),
            'sensorgroup' : QIcon(QPixmap(Icons.sensorgroup)),
            'sensor'      : QIcon(QPixmap(Icons.sensor)),
            'graph'       : QIcon(QPixmap(Icons.graph))
        }


    def addDatabase(self, folder):
        db = DataBaseRoot(folder)
        self.databases[folder] = db
        dbItem = QStandardItem(folder)
        dbItem.setData(QVariant(folder))
        dbItem.setIcon(self.icons['database'])
        self.rootItem.appendRow(dbItem)
        self._addProjects(db, dbItem, folder)

    def _addProjects(self, db, parent, dbf):
        for k, v in db.items():
            item = QStandardItem(k)
            item.setIcon(self.icons['project'])
            item.setData(QVariant(dbf+'|'+v.path))
            parent.appendRow(item)
            self._addSensorGroups(v, item, dbf)


    def _addSensorGroups(self, pr, parent, dbf):
        for k, v in pr.items():
            item = QStandardItem(k)
            item.setIcon(self.icons['sensorgroup'])
            item.setData(QVariant(dbf+'|'+v.path))
            parent.appendRow(item)
            self._addSensors(v, item, dbf)

    def _addSensors(self, sg, parent, dbf):
        for k, v in sg.items():
            item = QStandardItem(k)
            item.setIcon(self.icons['sensor'])
            item.setData(QVariant(dbf+'|'+v.path))
            parent.appendRow(item)
            #self._addSensors(v, item, dbf)
