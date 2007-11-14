# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""TextEditor PlugIn for SimuVis4 - provides simple text editing"""

import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn
from SimuVis4.SubWinManager import SubWinManager
from PyQt4.QtGui import QAction, QIcon, QWidget, QPixmap, QMenu, QFileDialog
from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject

class PlugIn(SimplePlugIn):

    def load(self):
        import GraphicsWindow, Items
        self.GraphicsWindow = GraphicsWindow
        self.Items = Items
        xpm = QPixmap()
        xpm.loadFromData(self.getFile('graphicswin.xpm').read())
        winIcon = QIcon(xpm)
        self.winManager = SubWinManager(SimuVis4.Globals.mainWin.workSpace, self.GraphicsWindow.GraphicsWindow,
            QCoreApplication.translate('Graphics', "GraphicsView"), winIcon)
        testAction = QAction(winIcon,
            QCoreApplication.translate('Graphics', '&Graphics Test'), SimuVis4.Globals.mainWin)
        testAction.setStatusTip(QCoreApplication.translate('Graphics', 'Show a new graphics window'))
        QWidget.connect(testAction, SIGNAL("triggered()"), self.test)
        SimuVis4.Globals.mainWin.plugInMenu.addAction(testAction)


    def unload(self, fast):
        if self.winManager:
            self.winManager.shutdown()
            del self.winManager


    def test(self):
        if not self.winManager:
            return
        from PyQt4.QtGui import QGraphicsScene, QGraphicsItem, QGraphicsLineItem
        from PyQt4.QtCore import QRectF, QLineF
        w = self.winManager.newWindow()
        scene = QGraphicsScene(w.graphicsView)
        scene.addItem(Items.Grid())
        scene.addItem(Items.Axes())

        line = scene.addLine(QLineF(0, 0, 0, 0))

        cross = Items.NodeCross(movable=True)
        cross.addEdge(line, 1)
        scene.addItem(cross)

        help = scene.addText(QCoreApplication.translate('Graphics', 'Press "h" for help!'))
        help.moveBy(-50, 80)

        text = Items.NodeText(QCoreApplication.translate('Graphics', 'Drag Me!'))
        text.setFlag(QGraphicsItem.ItemIsMovable, True)
        text.setFlag(QGraphicsItem.ItemIsSelectable, True)
        text.addEdge(line, 2)
        scene.addItem(text)
        w.graphicsView.setScene(scene)


    def listWindows(self):
        if self.winManager:
            return self.winManager.windows
