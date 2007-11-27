from PyQt4.QtGui import QGraphicsScene, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem,\
    QGraphicsEllipseItem, QPen, QBrush, QColor, QMenu
from PyQt4.QtCore import QRectF, QPointF, QLineF, QTimer, Qt
from math import sin, pi

SimTools = mainWin.plugInManager.getPlugIn('SimTools')
Graphics = mainWin.plugInManager.getPlugIn('Graphics')
if not (SimTools and Graphics):
    from SimuVis4.Errors import PlugInMissingError
    raise PlugInMissingError("Could not find needed PlugIns (SimTools, Graphics)!")


class Pendulum(object):
    """ abstract pendulum class """
    def __init__(self, **kw):
        self.initValues = kw
        F = SimTools.Quantities.Float
        self.mass =     F('mass', kw.get('mass', 1.0), descr='mass of ball', unit='kg', min=0.01, max=1000.0)
        self.length =   F('length', kw.get('length', 1.0), descr='length of rod', unit='m', min=0.01, max=1000.0)
        self.radius =   F('radius', kw.get('radius', 1.0), descr='radius of ball', unit='m', min=0.01, max=1000.0)
        self.gravity =  F('gravity', kw.get('gravity', 9.81), descr='gravity', unit='m/s²', min=0.01, max=1000.0)
        self.phi =      F('phi', kw.get('phi', 0.0), descr='angle of pendulum', unit='', min=-1.0e+6, max=1.0e+6)
        self.omega =    F('omega', kw.get('omega', 100.0), descr='angular speed', unit='1/s', min=0.0, max=1.0e+6)
        self.friction = F('friction', kw.get('friction', 0.05), descr='friction coefficient', unit='', min=0, max=100.0)
        self.time = 0
        self.lastStep = 0
        self.phiStep = 0

    def reset(self):
        self.time = 0
        self.phi.set(self.initValues['phi'])
        self.omega.set(self.initValues['omega'])

    def setState(self, phi, omega):
        self.phi.set(phi)
        self.omega.set(omega)
        self.time = self.timeFunc()

    def step(self, time):
        if time == 0:
            self.reset()
        self.update(time-self.time)
        self.time = time

    def update(self, timeStep):
        self.lastStep = timeStep
        theta = self.mass.v * (2.0/5.0 * self.radius.v*self.radius.v + self.length.v*self.length.v)
        lx = self.length.v* sin(pi*self.phi.v/180.0)
        M_total = -self.gravity.v * self.mass.v * lx - self.friction.v * self.omega.v
        self.omega.add(180.0/pi * timeStep * (M_total / theta))
        self.phiStep = timeStep * self.omega.v
        self.phi.add(self.phiStep)


class GPendulum(Graphics.Items.ItemGroupBase):
    def _setup(self):
        self.rod = QGraphicsLineItem(QLineF(0, 0, 0, 100))
        p = QPen(QColor(100, 100, 100))
        p.setWidth(5)
        self.rod.setPen(p)
        self.rod.setToolTip('This is the rod of the pendulum')
        self.ball = QGraphicsEllipseItem(QRectF(-20, 80, 40, 40))
        b = QBrush(Qt.SolidPattern)
        b.setColor(QColor(0, 255, 0))
        self.ball.setBrush(b)
        self.ball.setToolTip('This is the ball of the pendulum where the mass is concentrated')
        self.addToGroup(self.rod)
        self.addToGroup(self.ball)
        self.setFlags(QGraphicsItem.ItemIsSelectable)

    def setQuantities(self, q):
        self.quantities = q

    def contextMenuEvent(self, e):
        e.accept()
        m = QMenu()
        p = m.addAction("Properties");
        a = m.exec_(e.screenPos())
        if a == p:
            dlg = SimTools.Widgets.SimpleQuantitiesDialog(mainWin, 'Pendulum properties')
            dlg.addQuantities(self.quantities)
            dlg.exec_()


class PendulumGraphics(Pendulum):
    """pendulum which renders itself in a QGraphicsView"""

    def initGraphics(self, gView):
        self.gView = gView
        self.gScene = QGraphicsScene(self.gView)
        self.gView.setScene(self.gScene)

        self.gText = QGraphicsTextItem("Pendulum")
        self.gText.moveBy(0, -120)
        self.gGrid = Graphics.Items.Grid(size=(-140, -140, 140, 140), xstep=20, ystep=20,
            toolTip='the main grid')
        self.gCross = Graphics.Items.CrossX(toolTip='this is the fix point of the pendulum')
        self.gAxes = Graphics.Items.Axes(toolTip='theese are x,y-axes')
        self.gPendulum = GPendulum()
        self.gPendulum.setQuantities((self.mass, self.length, self.radius, self.gravity,
            self.omega, self.friction))
        self.gScene.addItem(self.gGrid)
        self.gScene.addItem(self.gText)
        self.gScene.addItem(self.gCross)
        self.gScene.addItem(self.gAxes)
        self.gScene.addItem(self.gPendulum)
        self.gView.setSceneRect(QRectF(-140, -140, 280, 280))
        self.gPendulum.rotate(self.phi.v)

    def reset(self):
        self.gPendulum.rotate(self.initValues['phi']-self.phi.v)
        Pendulum.reset(self)

    def update(self, timeStep):
        Pendulum.update(self, timeStep)
        self.gPendulum.rotate(self.phiStep)


graphWin = Graphics.winManager.newWindow("Pendel")

pendulum = PendulumGraphics(length=5, phi=-90, omega=228.00)
pendulum.initGraphics(graphWin.graphicsView)

timerWin = SimTools.Widgets.TimeSignalWindow(mainWin.workSpace)
mainWin.workSpace.addSubWindow(timerWin)
timerWin.show()
timerWin.timeSignalWidget.functions.append(pendulum.step)
timerWin.timeSignalWidget.frequencyInput.setValue(40.0)
timerWin.timeSignalWidget.compValueStepInput.setValue(0.1)
