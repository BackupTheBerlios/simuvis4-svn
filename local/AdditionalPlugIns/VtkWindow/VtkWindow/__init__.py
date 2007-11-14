# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""VTKWindow is a SimuVis4 plugin to get a VTK subwindow"""

import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn
from SimuVis4.SubWinManager import SubWinManager
from PyQt4.QtGui import QAction, QIcon, QWidget, QPixmap
from PyQt4.QtCore import SIGNAL, QCoreApplication, QTranslator

class PlugIn(SimplePlugIn):

    def load(self):
        self.initTranslations()
        import vtk, VtkWidget, VtkWindow, Objects, Helpers
        self.vtk = vtk
        self.VtkWidget = VtkWidget
        self.VtkWindow = VtkWindow
        self.Objects = Objects
        self.Helpers = Helpers
        xpm = QPixmap()
        xpm.loadFromData(self.getFile('3dwin.xpm').read())
        winIcon = QIcon(xpm)
        self.winManager = SubWinManager(SimuVis4.Globals.mainWin.workSpace, self.VtkWindow.VtkWindow,
                QCoreApplication.translate('VtkWindow', "Vtk Window"), winIcon)
        testAction = QAction(winIcon,
            QCoreApplication.translate('VtkWindow', '&VtkWindow Test'), SimuVis4.Globals.mainWin)
        testAction.setStatusTip(QCoreApplication.translate('VtkWindow', 'Show a new Vtk test window'))
        QWidget.connect(testAction, SIGNAL("triggered()"), self.test)
        SimuVis4.Globals.mainWin.plugInMenu.addAction(testAction)


    def unload(self, fast):
        if self.winManager:
            self.winManager.shutdown()
            del self.winManager


    def test(self, name=None):
        if not self.winManager:
            return

        w = self.winManager.newWindow(name)
        vtk = self.vtk

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
        #w.makeToolBar()
        w.show()
        w.vtkWidget.Initialize()
        w.vtkWidget.Start()

        return w
