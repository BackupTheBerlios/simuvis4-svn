# encoding: latin-1
# version:  $Id: Main.py,v 1.4 2007/08/13 09:16:52 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
import SimuVis4.Globals as glb
import BuildingData, BuildingTypes, ProjectFile

from PyQt4.QtGui import QAction, QIcon, QMenu, QGraphicsScene, QGraphicsLineItem, QGraphicsItem
from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject, QLineF, Qt, QRectF


def makeMenu():
    menu = QMenu('LNB Kühllastsimulation')

    newProjectAction = QAction(QIcon(), 'Neues Projekt', glb.mainWin)
    newProjectAction.setStatusTip('Erzeuge ein neues Projekt zur Kühllastsimulation')
    QObject.connect(newProjectAction, SIGNAL("triggered()"), newProject)
    menu.addAction(newProjectAction)

    loadProjectAction = QAction(QIcon(), 'Projekt laden', glb.mainWin)
    loadProjectAction.setStatusTip('Lade ein bestehendes Projekt zur Kühllastsimulation')
    QObject.connect(loadProjectAction, SIGNAL("triggered()"), loadProject)
    menu.addAction(loadProjectAction)

    return menu


def loadProject():
    raise SimuVis4.Errors.NotImplementedError('hier fehlt noch was...')


def newProject():
    bdata = BuildingTypes.OneZone()
    drawWalls(bdata)
    ws = glb.mainWin.workSpace
    simTools = glb.mainWin.plugInManager.getPlugIn('SimTools')
    win = simTools.Widgets.ProcessWindow(ws)
    ws.addWindow(win)
    win.show()


def drawWalls(bdata):
    """Test der Repräsentation von Wänden im QGraphicsView"""
    Graphics = glb.mainWin.plugInManager.getPlugIn('Graphics')
    graphWin = Graphics.manager.newWindow("Wandtest")
    graphScene = QGraphicsScene(graphWin.graphicsView)
    graphWin.graphicsView.setScene(graphScene)

    graphScene.addItem(Graphics.Items.Grid())

    for j in bdata.zone[0].joint:
        node = Graphics.Items.NodeEllipse(QRectF(-1, -1, 2, 2))
        node.setFlag(QGraphicsItem.ItemIsMovable, True)
        graphScene.addItem(node)
        j._node = node

    for w in bdata.zone[0].wall:
        line = QGraphicsLineItem()
        graphScene.addItem(line)
        w._line = line
        joints = [j for j in bdata.zone[0].joint if w in j.wall]
        joints[0]._node.addEdge(line, 1)
        joints[1]._node.addEdge(line, 2)

    for j in bdata.zone[0].joint:
        j._node.moveBy(j.x*10, j.y*10)

