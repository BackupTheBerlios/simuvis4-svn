# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QTimer, SIGNAL, QDateTime
from UI.DSChartMplToolBar import Ui_DSChartMplToolBar

mplBackend = SimuVis4.Globals.plugInManager['MatPlot'].backend_sv4agg
mplWinCount = SimuVis4.Misc.Counter(1000)

unitFactors = [60, 3600, 86400, 604800, 2592000, 31536000]


class ChartToolBar(QWidget, Ui_DSChartMplToolBar):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.LengthInput.setValue(1)
        self.LengthUnitInput.setCurrentIndex(2)
        self.startTime = 0
        self.blockUpdates = True
        self.connect(self.LengthInput, SIGNAL('valueChanged(int)'), self.lengthChanged)
        self.connect(self.LengthUnitInput, SIGNAL('activated(int)'), self.lengthUnitChanged)
        self.connect(self.StartInput, SIGNAL('dateTimeChanged(QDateTime)'), self.startChanged)
        self.connect(self.GoStartButton, SIGNAL('clicked()'), self.goStart)
        self.connect(self.GoBackButton, SIGNAL('clicked()'), self.goBack)
        self.connect(self.GoForwardButton, SIGNAL('clicked()'), self.goForward)
        self.connect(self.GoEndButton, SIGNAL('clicked()'), self.goEnd)
        self.connect(self.AnimationButton, SIGNAL('toggled(bool)'), self.animate)
        self.connect(self.AnimationDelayInput, SIGNAL('valueChanged(int)'), self.setAnimationDelay)
        self.connect(self.timer, SIGNAL('timeout()'), self.goForward)


    def setChartCanvas(self, chart, canvas):
        self.chart = chart
        self.canvas = canvas
        self.LengthInput.setValue(100)
        self.LengthUnitInput.setCurrentIndex(2)
        self.startTime = chart.sensorgroup.start
        dt =QDateTime()
        dt.setTime_t(self.startTime)
        self.StartInput.setDateTime(dt)
        self.blockUpdates = False
        self.showChart()


    def go(self, p, rel=True):
        if rel:
            t = self.StartInput.dateTime().toTime_t()
        else:
            t = 0
        # FIXME: check to not leave the data time range
        dt = QDateTime()
        dt.setTime_t(t + p)
        self.StartInput.setDateTime(dt)


    def goStart(self):
        self.go(self.chart.sensorgroup.start, False)


    def goBack(self):
        self.go(-self.chart.timeslice)


    def goForward(self):
        self.go(self.chart.timeslice)


    def goEnd(self):
        self.go(self.chart.sensorgroup.stop-self.chart.timeslice, False)


    def animate(self, a):
        if a and not self.timer.isActive():
                self.timer.start()
        else:
            self.timer.stop()


    def setAnimationDelay(self, v):
        self.timer.setInterval(1000*v)


    def lengthChanged(self, l):
        self.setTimeslice(l * unitFactors[self.LengthUnitInput.currentIndex()])


    def lengthUnitChanged(self, i):
        self.setTimeslice(unitFactors[i] * self.LengthInput.value())


    def startChanged(self, dt):
        self.startTime = dt.toTime_t()
        self.showChart()


    def setTimeslice(self, ts):
        if not ts == self.chart.timeslice:
            self.chart.setTimeslice(ts)
            self.showChart()


    def showChart(self):
        if self.blockUpdates:
            return
        self.chart.figure.clf()
        ## print "|||", self.startTime, self.chart.timeslice
        self.chart.makePlot(self.startTime)
        self.canvas.draw()



def showChartMplWindow(chart):
    canvas = mplBackend.FigureCanvasSV4(chart.figure)
    manager = mplBackend.FigureManagerSV4(canvas, mplWinCount())
    manager.window.dsToolBar = ChartToolBar(manager.window)
    manager.window.dsToolBar.setChartCanvas(chart, canvas)
    manager.window.mainLayout.insertWidget(0, manager.window.dsToolBar, 0)
    manager.window.show()

