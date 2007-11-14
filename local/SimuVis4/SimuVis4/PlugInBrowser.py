# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from SubWin import SubWindow
from UI.PlugInBrowser import Ui_PlugInBrowserWidget
import Globals, os, weakref

# FIXME: make this work !

states = {-1: "ERROR", 0: "UNKNOWN", 1: "LOADED", 2: "INITIALIZED"}

class PlugInBrowserWidget(QWidget, Ui_PlugInBrowserWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)


class PlugInProxyItem(QTreeWidgetItem):

    def setPlugIn(self, pi):
        self._pi = weakref.ref(pi)

    def data(self, col, role):
        if role != Qt.DisplayRole:
            return QVariant()
        pi = self._pi()
        if not pi:
            # FIXME: no longer needed ...
            return ''
        if col == 0:
            val = states.get(pi.state)
        elif col == 1:
            val = pi.name
        elif col == 2:
            val = pi.version
        elif col == 3:
            val = pi.description
        elif col == 4:
            val = pi.path
        return QVariant(QString(val))


class PlugInBrowser(SubWindow):

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        icon = QIcon(QPixmap(os.path.join(Globals.config['main:system_picture_path'], 'pibrowser.xpm')))
        self.setWindowIcon(icon)
        self.setWindowTitle(QCoreApplication.translate('PlugInBrowser', 'PlugIns'))
        self.browser = PlugInBrowserWidget(self)
        self.mainLayout.addWidget(self.browser)
        self.setFocusProxy(self.browser)
        self.plugInManager = Globals.mainWin.plugInManager

        self.toggleVisibleAction.setIcon(icon)
        self.toggleVisibleAction.setText(QCoreApplication.translate('PlugInBrowser', 'PlugIn &browser'))
        ##self.toggleVisibleAction.setShortcut(QCoreApplication.translate('PlugInBrowser', "Ctrl+B"))
        self.toggleVisibleAction.setStatusTip(QCoreApplication.translate('PlugInBrowser', 'PlugIn Browser'))
        self.updateList()


    def updateList(self):
        il = []
        for pi in self.plugInManager.plugIns.values():
            i = PlugInProxyItem(QTreeWidgetItem.UserType)
            i.setPlugIn(pi)
            il.append(i)
        self.browser.PlugInView.insertTopLevelItems(0, il)
