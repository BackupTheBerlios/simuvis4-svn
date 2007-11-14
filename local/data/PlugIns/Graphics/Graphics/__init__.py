# encoding: latin-1
# version:  $Id: __init__.py,v 1.8 2007/08/13 09:16:52 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""TextEditor PlugIn for SimuVis4 - provides simple text editing"""

myname = "Graphics"
proxy = None
Items = None 
manager = None

import SimuVis4.Globals
from SimuVis4.SubWinManager import SubWinManager
from PyQt4.QtGui import QAction, QIcon, QWidget, QPixmap, QMenu, QFileDialog
from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject

logger = SimuVis4.Globals.logger


def plugInInit(p):
    global proxy, manager, Items
    import GraphicsWindow
    import Items
    proxy = p
    xpm = QPixmap()
    xpm.loadFromData(proxy.openFile('graphicswin.xpm').read())
    winIcon = QIcon(xpm)
    manager = SubWinManager(SimuVis4.Globals.mainWin.workSpace, GraphicsWindow.GraphicsWindow,
        QCoreApplication.translate('Graphics', "GraphicsView"), winIcon)
    testAction = QAction(winIcon,
        QCoreApplication.translate('Graphics', '&Graphics Test'), SimuVis4.Globals.mainWin)
    testAction.setStatusTip(QCoreApplication.translate('Graphics', 'Show a new graphics window'))
    QWidget.connect(testAction, SIGNAL("triggered()"), test)
    SimuVis4.Globals.mainWin.plugInMenu.addAction(testAction)


def plugInExitOk():
    return True


def plugInExit(fast):
    global manager
    if manager:
        manager.shutdown()
        del manager
    manager = None


def test():
    if not manager:
        return
    from PyQt4.QtGui import QGraphicsScene, QGraphicsItem, QGraphicsLineItem
    from PyQt4.QtCore import QRectF, QLineF
    w = manager.newWindow()
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


def listWindows():
    if manager:
        return manager.windows
