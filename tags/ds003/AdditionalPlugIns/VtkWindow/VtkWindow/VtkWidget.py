# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VtkWidget(QVTKRenderWindowInteractor):
    """ in the future there will be some additional functions """
    pass


if __name__ == "__main__":
    """A simple example that uses the VtkWidget class.  """
    from PyQt4.QtGui import QApplication
    import vtk

    app = QApplication(['VtkWidget'])

    widget = VtkWidget()
    widget.Initialize()
    widget.Start()
    # if you dont want the 'q' key to exit comment this.
    widget.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

    ren = vtk.vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)

    cone = vtk.vtkConeSource()
    cone.SetResolution(16)

    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())

    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)

    ren.AddActor(coneActor)

    # show the widget
    widget.show()
    app.exec_()

