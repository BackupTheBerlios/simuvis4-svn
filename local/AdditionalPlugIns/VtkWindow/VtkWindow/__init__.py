# encoding: latin-1
# version:  $Id: __init__.py,v 1.12 2007/08/13 09:16:52 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""VTKWindow is a SimuVis4 plugin to get a VTK subwindow"""

import SimuVis4.Globals
import SimuVis4.Misc
from SimuVis4.SubWinManager import SubWinManager
from PyQt4.QtGui import QAction, QIcon, QWidget, QPixmap
from PyQt4.QtCore import SIGNAL, QCoreApplication, QTranslator

myName = 'VtkWindow'
proxy  = None
manager = None
vtk = None

VtkWidget = None
VtkWindow = None
Objects = None
Helpers = None
translator = None

def plugInInit(p):
    global proxy, manager, vtk, VtkWidget, VtkWindow, Objects, Helpers, translator
    proxy = p
    import vtk, VtkWidget, VtkWindow, Objects, Helpers
    if SimuVis4.Globals.language:
        try:
            translator = QTranslator()
            translator.load(proxy.openFile('%s.qm' % SimuVis4.Globals.language).read())
            SimuVis4.Globals.application.installTranslator(translator)
        except:
            pass
    xpm = QPixmap()
    xpm.loadFromData(proxy.openFile('3dwin.xpm').read())
    winIcon = QIcon(xpm)
    manager = SubWinManager(SimuVis4.Globals.mainWin.workSpace, VtkWindow.VtkWindow,
        QCoreApplication.translate('VtkWindow', "Vtk Window"), winIcon)
    testAction = QAction(winIcon,
        QCoreApplication.translate('VtkWindow', '&VtkWindow Test'), SimuVis4.Globals.mainWin)
    testAction.setStatusTip(QCoreApplication.translate('VtkWindow', 'Show a new Vtk test window'))
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
    if translator:
        SimuVis4.Globals.application.removeTranslator(translator)


def test(name=None):
    if not manager:
        return

    w = manager.newWindow(name)

    ren = vtk.vtkRenderer()
    w.vtkWidget.GetRenderWindow().AddRenderer(ren)

    sphere = vtk.vtkSphereSource()
    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInput(sphere.GetOutput())
    sphereActor = vtk.vtkActor()
    sphereActor.SetMapper(sphereMapper)
    sphereActor.GetProperty().SetColor(1.0, 0.3, 0.3)
    ren.AddActor(sphereActor)

    cone = vtk.vtkConeSource()
    cone.SetResolution(16)
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.AddPosition(0.0, 1.0, 0.0)
    coneActor.GetProperty().SetColor(1.0, 1.0, 0.0)
    ren.AddActor(coneActor)

    cube = vtk.vtkCubeSource()
    cubeMapper = vtk.vtkPolyDataMapper()
    cubeMapper.SetInput(cube.GetOutput())
    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(cubeMapper)
    cubeActor.AddPosition(0.0, 2.0, 0.0)
    cubeActor.GetProperty().SetColor(0.3, 1.0, 0.3)
    ren.AddActor(cubeActor)
    w.makeToolBar()
    w.show()
    w.vtkWidget.Initialize()
    w.vtkWidget.Start()
    

    return w
