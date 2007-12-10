# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os, Icons, string
from PyQt4.QtGui import QWidget, QTreeView, QAbstractItemView, QStandardItemModel, QStandardItem, \
    QVBoxLayout, QHBoxLayout, QSplitter, QTextBrowser, QMessageBox, QToolButton, QIcon, QPixmap, \
    QFrame, QFileDialog, QPen
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt, SIGNAL, QCoreApplication
from PyQt4.Qwt5 import QwtPlotCurve

from datastorage.database import DataBaseRoot, Sensor

mplBackend = SimuVis4.Globals.plugInManager['MatPlot'].backend_sv4agg
mplWinCount = SimuVis4.Misc.Counter(1000)


rootInfo = string.Template(str(QCoreApplication.translate('DataStorageBrowser', """
<h3>Root $name</h3>
<table border="1">
<tr><td>Title</td><td>$title</td></tr>
<tr><td>Folder</td><td>$folder</td></tr>
<tr><td>Projects</td><td>$projects</td></tr>
</table>
""")))


projectInfo = string.Template(str(QCoreApplication.translate('DataStorageBrowser', """
<h3>Project $name</h3>
<table border="1">
<tr><td>Title</td><td>$title</td></tr>
<tr><td>Groups</td><td>$groups</td></tr>
</table>
""")))


groupInfo = string.Template(str(QCoreApplication.translate('DataStorageBrowser', """
<h3>Group $name</h3>
<table border="1">
<tr><td>Title</td><td>$title</td></tr>
<tr><td>Sensors</td><td>$sensors</td></tr>
<tr><td>Charts</td><td>$charts</td></tr>
</table>
""")))


sensorInfo = string.Template(str(QCoreApplication.translate('DataStorageBrowser', """
<h3>Sensor $name</h3>
<table border="1">
<tr><td>Title</td><td>$title</td></tr>
<tr><td>Start</td><td>$start</td></tr>
<tr><td>Stop</td><td>$stop</td></tr>
<tr><td>Step</td><td>$step</td></tr>
<tr><td>Length</td><td>$length</td></tr>
</table>
Double click on the sensor item to show a chart!
""")))


chartInfo = string.Template(str(QCoreApplication.translate('DataStorageBrowser', """
<h3>Chart $name</h3>
Double click on the chart item to show!
""")))


metaDataStartInfo = str(QCoreApplication.translate('DataStorageBrowser', """
<h4>Metadata</h4>
<table border="1">
"""))


metaDataLineInfo = string.Template("""
<tr><td>$name</td><td>$value</td></tr>
""")


metaDataEndInfo = """
</table>
"""


def formatMetaData(n):
    keys = n.getMetaKeys()
    if not keys:
        return ""
    l = [metaDataStartInfo]
    for k in keys:
        l.append(metaDataLineInfo.substitute(name=k, value=n.getMetaData(k)))
    l.append(metaDataEndInfo)
    return '\n'.join(l)


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
        p = str(item.data().toString()).split('|')
        if p[0] == 'R': # root
            x = self.model.databases[p[1]]
        elif p[0] in 'PGS': # project, group, sensor
            x = self.model.databases[p[1]].find(p[2])
        elif p[0] == 'C': # chart
            x = self.model.databases[p[1]].find(p[2]).charts[p[3]]
        return p[0], x


    def showItem(self, mi, pr):
        t, n = self.node(mi)
        print t, dir(n)
        txt = ""
        if t == 'R':
            # FIXME: no metadata?
            txt = rootInfo.substitute(name=n.name, title=n.title, folder=n.h5dir, projects=len(n)) #+ formatMetaData(n)
        elif t == 'P':
            txt = projectInfo.substitute(name=n.name, title=n.title, groups=len(n)) + formatMetaData(n)
        elif t == 'G':
            txt = groupInfo.substitute(name=n.name, title=n.title, sensors=len(n), charts=len(n.charts)) + formatMetaData(n)
        elif t == 'S':
            txt = sensorInfo.substitute(name=n.name, title=n.title, start=n.timegrid.start, stop=n.timegrid.stop,
                step=n.timegrid.step, length=n.datalen()) + formatMetaData(n)
        elif t == 'C':
            txt = chartInfo.substitute(name=n.name)
        self.textBrowser.setText(txt)


    def itemAction(self, mi):
        t, n = self.node(mi)
        if t == 'R':
            pass
        elif t == 'P':
            pass
        elif t == 'G':
            pass
        elif t == 'S':
            # Sensor: show a new QwtPlot window 
            w = SimuVis4.Globals.mainWin.plugInManager['QwtPlot'].winManager.newWindow(n.path)
            curve = QwtPlotCurve(n.name)
            curve.setData(n.timegrid.getTimeArray(), n[:].filled())
            curve.setPen(QPen(Qt.blue))
            curve.attach(w.plot)
            w.plot.replot()
            w.plot.zoomer.setZoomBase()
        elif t == 'C':
            # Chart: show the chart 
            n.figure.clf()
            canvas = mplBackend.FigureCanvasSV4(n.figure)
            manager = mplBackend.FigureManagerSV4(canvas, mplWinCount())
            n.makePlot(None)
            canvas.draw()
            manager.window.show()


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
        dbItem = QStandardItem(db.name)
        dbItem.setData(QVariant("R|%s" % folder))
        dbItem.setIcon(self.icons['database'])
        self.rootItem.appendRow(dbItem)
        self._addDB(db, dbItem, folder)

    def _addDB(self, db, parent, dbf):
        for k, v in db.items():
            item = QStandardItem(k)
            item.setIcon(self.icons['project'])
            item.setData(QVariant("P|%s|%s" % (dbf, v.path)))
            parent.appendRow(item)
            self._addProject(v, item, dbf)

    def _addProject(self, pr, parent, dbf):
        for k, v in pr.items():
            item = QStandardItem(k)
            item.setIcon(self.icons['sensorgroup'])
            item.setData(QVariant("G|%s|%s" % (dbf, v.path)))
            parent.appendRow(item)
            self._addSensorGroup(v, item, dbf)

    def _addSensorGroup(self, sg, parent, dbf):
        for k, v in sg.items():
            item = QStandardItem(k)
            item.setIcon(self.icons['sensor'])
            item.setData(QVariant("S|%s|%s" % (dbf, v.path)))
            parent.appendRow(item)
        for k, v in sg.charts.items():
            item = QStandardItem(k)
            item.setIcon(self.icons['graph'])
            item.setData(QVariant("C|%s|%s|%s" % (dbf, sg.path, k)))
            parent.appendRow(item)
