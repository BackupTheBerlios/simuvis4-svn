# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""
A simple VTK input file for PyQt, the qt bindings for python.
See http://www.trolltech.com for qt documentation, and
http://www.river-bank.demon.co.uk or http://www.thekompany.com
for the qt python bindings.

This class is based on the vtkGenericRenderWindowInteractor and is
therefore fairly powerful.  It should also play nicely with the
vtk3DWidget code.

Created by Prabhu Ramachandran, May 2002
Based on David Gobbi's QVTKRenderWidget.py

Changes by Gerard Vermeulen Feb. 2003
 Win32 support.

Changes by Gerard Vermeulen, May 2003
 Bug fixes and better integration with the Qt framework.

Changes by Joerg Raedler, Oct 2006
 Changed to work with Qt4/PyQt4.
"""

"""
This class works with the UNIX and Win32 versions of Qt.

Depending on the OpenGL graphics drivers, it may not
be possible to have more than one QVTKRenderWidget
per application.

In short, this class is experimental.
"""


# To do for Win32:
# 1. More testing to assure that the widget is always cleaned up
#    properly and does not crash the application.

from PyQt4.QtCore import Qt, QTimer, SIGNAL
from PyQt4.QtGui import QWidget, QApplication

import vtk

class VtkWidget(QWidget):

    """ A QVTKRenderWindowInteractor for Python and Qt.  Uses a
    vtkGenericRenderWindowInteractor to handle the interactions.  Use
    GetRenderWindow() to get the vtkRenderWindow.  Create with the
    keyword stereo=1 in order to generate a stereo-capable window.

    The user interface is summarized in vtkInteractorStyle.h:

    - Keypress j / Keypress t: toggle between joystick (position
    sensitive) and trackball (motion sensitive) styles. In joystick
    style, motion occurs continuously as long as a mouse button is
    pressed. In trackball style, motion occurs when the mouse button
    is pressed and the mouse pointer moves.

    - Keypress c / Keypress o: toggle between camera and object
    (actor) modes. In camera mode, mouse events affect the camera
    position and focal point. In object mode, mouse events affect
    the actor that is under the mouse pointer.

    - Button 1: rotate the camera around its focal point (if camera
    mode) or rotate the actor around its origin (if actor mode). The
    rotation is in the direction defined from the center of the
    renderer's viewport towards the mouse position. In joystick mode,
    the magnitude of the rotation is determined by the distance the
    mouse is from the center of the render window.

    - Button 2: pan the camera (if camera mode) or translate the actor
    (if object mode). In joystick mode, the direction of pan or
    translation is from the center of the viewport towards the mouse
    position. In trackball mode, the direction of motion is the
    direction the mouse moves. (Note: with 2-button mice, pan is
    defined as <Shift>-Button 1.)

    - Button 3: zoom the camera (if camera mode) or scale the actor
    (if object mode). Zoom in/increase scale if the mouse position is
    in the top half of the viewport; zoom out/decrease scale if the
    mouse position is in the bottom half. In joystick mode, the amount
    of zoom is controlled by the distance of the mouse pointer from
    the horizontal centerline of the window.

    - Keypress 3: toggle the render window into and out of stereo
    mode.  By default, red-blue stereo pairs are created. Some systems
    support Crystal Eyes LCD stereo glasses; you have to invoke
    SetStereoTypeToCrystalEyes() on the rendering window.  Note: to
    use stereo you also need to pass a stereo=1 keyword argument to
    the constructor.

    - Keypress e: exit the application.

    - Keypress f: fly to the picked point

    - Keypress p: perform a pick operation. The render window interactor
    has an internal instance of vtkCellPicker that it uses to pick. 

    - Keypress r: reset the camera view along the current view
    direction. Centers the actors and moves the camera so that all actors
    are visible.

    - Keypress s: modify the representation of all actors so that they
    are surfaces. 

    - Keypress u: invoke the user-defined function. Typically, this
    keypress will bring up an interactor that you can type commands in.

    - Keypress w: modify the representation of all actors so that they
    are wireframe.
    """

    
    def __init__(self, parent=None, stereo=False, rw=None):
        # the current button
        self._ActiveButton = 0

        # private attributes
        self.__oldFocus = None
        self.__saveX = 0
        self.__saveY = 0
        self.__saveState = 0

        QWidget.__init__(self, parent)
        self._RenderWindow = rw or vtk.vtkRenderWindow()

        if stereo:
            self._RenderWindow.StereoCapableWindowOn()
            self._RenderWindow.SetStereoTypeToCrystalEyes()

        self._Iren = vtk.vtkGenericRenderWindowInteractor()
        self._Iren.SetRenderWindow(self._RenderWindow)

        size = self.size()
        self._Iren.SetSize(size.width(), size.height())
        
        self._RenderWindow.SetWindowInfo(str(self.winId()))
        self._Iren.ConfigureEvent()

        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WA_PaintOnScreen)
        self.setAutoFillBackground(False)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        
        self._Timer = QTimer(self)
        self.connect(self._Timer, SIGNAL('timeout()'),
                     self.TimerEvent)

        self._Iren.AddObserver('CreateTimerEvent', self.CreateTimer)
        self._Iren.AddObserver('DestroyTimerEvent', self.DestroyTimer)

           
    def __getattr__(self, attr):
        """Makes the object behave like a
        vtkGenericRenderWindowInteractor"""
        if attr == '__vtk__':
            return lambda t=self._Iren: t
        elif hasattr(self._Iren, attr):
            return getattr(self._Iren, attr)
        elif hasattr(QWidget, attr):
            return getattr(self.sipThis, attr)
        else:
            raise AttributeError, self.__class__.__name__ + \
                  " has no attribute named " + attr


    def CreateTimer(self, obj, evt):
        self._Timer.start(10)

        
    def DestroyTimer(self, obj, evt):
        self._Timer.stop()
        return 1

        
    def TimerEvent(self):
        self._Iren.TimerEvent()

        
    def show(self):
        QWidget.show(self)
        self.update() # needed for initial contents display on Win32

        
    def paintEvent(self, ev):
        self.Render()

        
    def resizeEvent(self, ev):
        size = self.size()
        self._Iren.SetSize(size.width(), size.height())
        self._Iren.ConfigureEvent()
        self.update()

        
    def _GetCtrlShift(self, ev):
        ctrl, shift = 0, 0
        if hasattr(ev, 'state'):
            print ev.state()
            if (ev.state() & 8):
                shift = 1
            if (ev.state() & 16):
                ctrl = 1
        elif self.__saveState:
            if (self.__saveState & 8):
                shift = 1
            if (self.__saveState & 16):
                ctrl = 1            
        return ctrl, shift

        
    def enterEvent(self, ev):
        # FIXME: was this something important?
        #if not self.hasFocus():
            #self.__oldFocus = self.focusWidget()
            #self.setFocus()
        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, chr(0), 0, None)
        self._Iren.EnterEvent()


    def leaveEvent(self, ev):
        if (self.__saveState & 0x7) == 0 and self.__oldFocus:
            self.__oldFocus.setFocus()
            self.__oldFocus = None
        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, chr(0), 0, None)
        self._Iren.LeaveEvent()


    def mousePressEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), 0, None)

        self._ActiveButton = 0
        if ev.button() == 1:
            self._Iren.LeftButtonPressEvent()
            self._ActiveButton = 'Left'
        elif ev.button() == 2:
            self._Iren.RightButtonPressEvent()
            self._ActiveButton = 'Right'
        elif ev.button() == 4:
            self._Iren.MiddleButtonPressEvent()
            self._ActiveButton = 'Middle'

            
    def mouseReleaseEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), 0, None)
        
        if self._ActiveButton == 'Right':
            self._Iren.RightButtonReleaseEvent()
        elif self._ActiveButton == 'Left':
            self._Iren.LeftButtonReleaseEvent()
        elif self._ActiveButton == 'Middle':
            self._Iren.MiddleButtonReleaseEvent()

            
    def mouseMoveEvent(self, ev):
        #FIXME: was macht das, und warum geht es nicht mehr?  self.__saveState = ev.state()
        self.__saveX = ev.x()
        self.__saveY = ev.y()
        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), 0, None)
        self._Iren.MouseMoveEvent()

        
    def keyPressEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        key = chr(0)
        if ev.key() < 256:
            key = chr(ev.key())

        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, key, 0, None)
        self._Iren.KeyPressEvent()
        self._Iren.CharEvent()

        
    def keyReleaseEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        key = chr(0)
        if ev.key() < 256:
            key = chr(ev.key())

        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, key, 0, None)
        self._Iren.KeyReleaseEvent()

        
    def GetRenderWindow(self):
        return self._RenderWindow

        
    def Render(self):
        self._RenderWindow.Render()


if __name__ == "__main__":
    """A simple example that uses the QVTKRenderWindowInteractor
    class.  """
    
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

