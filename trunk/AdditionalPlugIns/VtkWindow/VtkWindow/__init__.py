# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""VTKWindow is a SimuVis4 plugin to get a VTK subwindow"""

import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn
from SimuVis4.SubWinManager import SubWinManager
from PyQt4.QtGui import QAction, QIcon, QWidget, QPixmap
from PyQt4.QtCore import SIGNAL, QCoreApplication, QTranslator

glb = SimuVis4.Globals

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
        self.winManager = SubWinManager(glb.mainWin.workSpace, self.VtkWindow.VtkWindow,
                QCoreApplication.translate('VtkWindow', "Vtk Window"), winIcon)
        testAction = QAction(winIcon,
            QCoreApplication.translate('VtkWindow', '&VtkWindow Test'), glb.mainWin)
        testAction.setStatusTip(QCoreApplication.translate('VtkWindow', 'Show a new Vtk test window'))
        QWidget.connect(testAction, SIGNAL("triggered()"), self.test)
        glb.mainWin.plugInMenu.addAction(testAction)

        ftActions = glb.fileTypeActions
        ftActions.addType('application/x-3ds', '.3ds')
        ftActions.addAction(self.show3DS, ('application/x-3ds',),
            QCoreApplication.translate('VtkWindow', 'Open in VtkWindow'), 5)
        ftActions.addType('application/x-vrml', '.wrl')
        ftActions.addAction(self.showVRML, ('application/x-vrml',),
            QCoreApplication.translate('VtkWindow', 'Open in VtkWindow'), 5)

        return True


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
        w.show()
        w.vtkWidget.Initialize()
        w.vtkWidget.Start()

        return w

    def show3DS(self, fileName):
        vtk = self.vtk
        importer = vtk.vtk3DSImporter()
        importer.ComputeNormalsOn()
        importer.SetFileName(fileName)
        importer.Read()
        ren = importer.GetRenderer()
        ren.SetBackground(0.1, 0.2, 0.4)
        ren.ResetCamera()
        w = self.winManager.newWindow(fileName)
        importer.SetRenderWindow(w.vtkWidget.GetRenderWindow())
        w.vtkWidget.GetRenderWindow().AddRenderer(ren)
        w.show()
        w.vtkWidget.Initialize()
        w.vtkWidget.Start()
        return w

    def showVRML(self, fileName):
        vtk = self.vtk
        importer = vtk.vtkVRMLImporter()
        importer.SetFileName(fileName)
        importer.Read()
        ren = importer.GetRenderer()
        ren.SetBackground(0.1, 0.2, 0.4)
        ren.ResetCamera()
        w = self.winManager.newWindow(fileName)
        importer.SetRenderWindow(w.vtkWidget.GetRenderWindow())
        w.vtkWidget.GetRenderWindow().AddRenderer(ren)
        w.show()
        w.vtkWidget.Initialize()
        w.vtkWidget.Start()
        return w
