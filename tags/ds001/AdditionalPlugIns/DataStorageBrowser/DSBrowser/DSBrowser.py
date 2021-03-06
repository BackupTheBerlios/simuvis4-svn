# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os, Icons, string
from PyQt4.QtGui import QWidget, QTreeView, QAbstractItemView, QStandardItemModel, QStandardItem, \
    QVBoxLayout, QHBoxLayout, QSplitter, QTextBrowser, QMessageBox, QToolButton, QIcon, QPixmap, \
    QFrame, QFileDialog, QPen, QMenu
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt, SIGNAL, QCoreApplication
from cgi import escape

from DSChartMpl import showChartMplWindow
from DSPlotQwt import showQwtPlotWindow
from DSMetadata import editMetadata
from DSAddChartMpl import showNewChartWizard

from datastorage.database import DataBaseRoot, Sensor

showChartMaximized = SimuVis4.Globals.config.getboolean('datastoragebrowser', 'show_chart_maximized')

rootInfo = string.Template(unicode(QCoreApplication.translate('DataStorageBrowser', """
<h3>Root $name</h3>
<table border="1">
<tr><td>Title</td><td>$title</td></tr>
<tr><td>Folder</td><td>$folder</td></tr>
<tr><td>Projects</td><td>$projects</td></tr>
</table>
""")))


projectInfo = string.Template(unicode(QCoreApplication.translate('DataStorageBrowser', """
<h3>Project $name</h3>
<table border="1">
<tr><td>Title</td><td>$title</td></tr>
<tr><td>Groups</td><td>$groups</td></tr>
</table>
""")))


groupInfo = string.Template(unicode(QCoreApplication.translate('DataStorageBrowser', """
<h3>Group $name</h3>
<table border="1">
<tr><td>Title</td><td>$title</td></tr>
<tr><td>Sensors</td><td>$sensors</td></tr>
<tr><td>Charts</td><td>$charts</td></tr>
</table>
""")))


sensorInfo = string.Template(unicode(QCoreApplication.translate('DataStorageBrowser', """
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


chartInfo = string.Template(unicode(QCoreApplication.translate('DataStorageBrowser', """
<h3>Chart $name</h3>
Double click on the chart item to show!
""")))


metaDataStartInfo = unicode(QCoreApplication.translate('DataStorageBrowser', """
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
        l.append(metaDataLineInfo.substitute(name=k, value=escape(unicode(n.getMetaData(k)))))
    l.append(metaDataEndInfo)
    return '\n'.join(l)



class DSBrowser(QWidget):
    """browser for datastorage databases
       Nodes are identified by a string, containing fields separated by '|'.
       - first filed is a capital letter:
       'R'oot, 'P'roject, sensor'G'roup, 'S'ensor and 'C'hart
       - second field is the database folder
       - third filed is the path of the node in the database
       - for charts the fourth field is the chart name (third is path of sensorgroup in this case)
    """
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
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.setAutoExpandDelay(500)
        self.textBrowser = QTextBrowser(self.splitter)
        self.layout.addWidget(self.splitter)
        self.splitter.setStretchFactor(0, 60)
        self.splitter.setStretchFactor(1, 40)
        self.model = DSModel()
        self.treeView.setModel(self.model)
        self.treeView.setSortingEnabled(True)
        self.treeView.expandAll()
        self.connect(self.treeView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.showItem)
        self.connect(self.treeView, SIGNAL("doubleClicked(QModelIndex)"), self.itemAction)
        self.connect(self.treeView, SIGNAL("customContextMenuRequested(QPoint)"), self.showContextMenu)
        self.selectedNode = None
        self.selectedMI = None


    def loadDatabase(self, dn=None):
        """load a database"""
        if not dn:
            dn = QFileDialog.getExistingDirectory(self, QCoreApplication.translate('DataStorageBrowser',
                "Select a folder containing a datastorage database"), SimuVis4.Globals.defaultFolder)
            if not dn.isEmpty():
                dn = unicode(dn)
                SimuVis4.Globals.defaultFolder = dn
            else:
                return
        self.model.addDatabase(dn)
        self.treeView.expandToDepth(1)


    def dropDatabases(self):
        # FIXME: implement it
        pass


    def showItem(self, mi, pr):
        """show the item at model index mi"""
        t, n = self.model.dsNode(mi)
        txt = ""
        if t == 'R':
            # FIXME: no metadata?
            txt = rootInfo.substitute(name=n.name, title=escape(n.title), folder=n.h5dir, projects=len(n)) # + formatMetaData(n)
        elif t == 'P':
            txt = projectInfo.substitute(name=n.name, title=escape(n.title), groups=len(n)) + formatMetaData(n)
        elif t == 'G':
            txt = groupInfo.substitute(name=n.name, title=escape(n.title), sensors=len(n), charts=len(n.charts)) + formatMetaData(n)
        elif t == 'S':
            txt = sensorInfo.substitute(name=n.name, title=escape(n.title), start=n.timegrid.start, stop=n.timegrid.stop,
                step=n.timegrid.step, length=n.datalen()) + formatMetaData(n)
        elif t == 'C':
            txt = chartInfo.substitute(name=n.name)
        self.textBrowser.setText(txt)


    def itemAction(self, mi):
        """default action (on doubleclick) for item at model index mi"""
        t, n = self.model.dsNode(mi)
        if t == 'R':
            pass
        elif t == 'P':
            pass
        elif t == 'G':
            pass
        elif t == 'S':
            print n
            self.showQwtPlot(n)
        elif t == 'C':
            self.showMplChart(n)


    def showContextMenu(self, pos):
        """show context menu for item at pos"""
        mi = self.treeView.indexAt(pos)
        t, n = self.model.dsNode(mi)
        self.selectedNode = n
        self.selectedMI = mi
        m = QMenu()
        if t in 'RPGS':
            p = m.addAction(QCoreApplication.translate('DataStorageBrowser', 'Edit metadata'), self.editMetadata)
        if t == 'R':
            pass
        elif t == 'P':
            pass
        elif t == 'G':
            m.addAction(QCoreApplication.translate('DataStorageBrowser', 'Add Chart'), self.newChart)
        elif t == 'S':
            m.addAction(QCoreApplication.translate('DataStorageBrowser', 'Plot (Qwt)'), self.showQwtPlot)
        elif t == 'C':
            m.addAction(QCoreApplication.translate('DataStorageBrowser', 'Show'), self.showMplChart)
            m.addAction(QCoreApplication.translate('DataStorageBrowser', 'Delete'), self.deleteItem)
        a = m.exec_(self.treeView.mapToGlobal(pos))


    def showMplChart(self, node=None):
        if node is None:
            node = self.selectedNode
        showChartMplWindow(node, maximized=showChartMaximized)


    def showQwtPlot(self, node=None):
        if node is None:
            node = self.selectedNode
        showQwtPlotWindow(node, maximized=showChartMaximized)


    def editMetadata(self, node=None):
        if node is None:
            node = self.selectedNode
        editMetadata(node)


    def newChart(self, mi=None):
        """add a chart to sensorgroup at mi using the wizard"""
        if mi is None:
            mi = self.selectedMI
        showNewChartWizard(self.model, mi)

    def deleteItem(self, mi=None):
        """delete the item at mi"""
        if mi is None:
            mi = self.selectedMI
        self.model.deleteItem(mi)


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
        """add the database at folder to the model"""
        db = DataBaseRoot(folder)
        self.databases[folder] = db
        dbItem = QStandardItem(db.name)
        dbItem.setData(QVariant("R|%s" % folder))
        dbItem.setIcon(self.icons['database'])
        self.rootItem.appendRow(dbItem)
        self._processDB(db, dbItem, folder)


    def _processDB(self, db, parent, dbf):
        """process the database and add its child nodes"""
        for k, v in db.items():
            item = QStandardItem(k)
            item.setIcon(self.icons['project'])
            item.setData(QVariant("P|%s|%s" % (dbf, v.path)))
            parent.appendRow(item)
            self._processProject(v, item, dbf)


    def _processProject(self, pr, parent, dbf):
        """process the project and add its child nodes"""
        for k, v in pr.items():
            item = QStandardItem(k)
            item.setIcon(self.icons['sensorgroup'])
            item.setData(QVariant("G|%s|%s" % (dbf, v.path)))
            parent.appendRow(item)
            self._processSensorGroup(v, item, dbf)


    def _processSensorGroup(self, sg, parent, dbf):
        """process the sensorgroup and add its child nodes"""
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


    def dsFolder(self, mi):
        """get the database folder name for a model index"""
        return str(self.itemFromIndex(mi).data().toString()).split('|')[1]


    def dsNode(self, mi):
        """get the type of the node and the node for a model index"""
        item = self.itemFromIndex(mi)
        p = str(item.data().toString()).split('|')
        if p[0] == 'R': # root
            x = self.databases[p[1]]
        elif p[0] in 'PGS': # project, group, sensor
            x = self.databases[p[1]].find(p[2])
        elif p[0] == 'C': # chart
            x = self.databases[p[1]].find(p[2]).charts[p[3]]
        return p[0], x


    def addChart(self, chart, mi):
        """add a new chart to sensorgroup item at mi"""
        t, sensorgroup = self.dsNode(mi)
        if not chart.name in sensorgroup.charts:
                sensorgroup.addChart(chart)
                sensorgroup.flush()
        chItem = QStandardItem(chart.name)
        chItem.setIcon(self.icons['graph'])
        chItem.setData(QVariant("C|%s|%s|%s" % (self.dsFolder(mi), sensorgroup.path, chart.name)))
        self.itemFromIndex(mi).appendRow(chItem)


    def deleteItem(self, mi):
        """delete the model item at mi and delete corresponding node from database"""
        t, node = self.dsNode(mi)
        item = self.itemFromIndex(mi)
        if t == 'C':
            node.sensorgroup.removeChart(node.name)
            node.sensorgroup.flush()
        # FIXME: remove sensors, sensorgroups or projects ?
        else:
            return
        item.parent().removeRow(item.row())
