# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, Icons
from PyQt4.QtGui import QWidget, QIcon, QPixmap
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
        self.GoStartButton.setIcon(QIcon(QPixmap(Icons.goStart)))
        self.GoBackButton.setIcon(QIcon(QPixmap(Icons.goBack)))
        self.GoForwardButton.setIcon(QIcon(QPixmap(Icons.goForward)))
        self.GoEndButton.setIcon(QIcon(QPixmap(Icons.goEnd)))
        self.AnimationButton.setIcon(QIcon(QPixmap(Icons.animation)))
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
        # FIXME: get a hint on the start time and display interval - from datastorage?
        self.startTime = chart.sensorgroup.start
        mindt =QDateTime()
        mindt.setTime_t(self.startTime)
        self.StartInput.setDateTime(mindt)
        maxdt = QDateTime()
        maxdt.setTime_t(chart.sensorgroup.stop)
        self.StartInput.setDateRange(mindt.date(), maxdt.date())
        self.LengthInput.setValue(100)
        self.LengthUnitInput.setCurrentIndex(2)
        self.blockUpdates = False
        self.updateChart()


    def go(self, p, rel=True):
        if rel:
            t = self.StartInput.dateTime().toTime_t()
        else:
            t = 0
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
        self.updateChart()


    def setTimeslice(self, ts):
        if not ts == self.chart.timeslice:
            maxdt = QDateTime()
            maxdt.setTime_t(self.chart.sensorgroup.stop-ts)
            self.StartInput.setMaximumDate(maxdt.date())
            self.chart.setTimeslice(ts)
            self.updateChart()


    def updateChart(self):
        if self.blockUpdates:
            return
        self.chart.figure.clf()
        self.chart.makePlot(self.startTime)
        self.canvas.draw()



def showChartMplWindow(chart, maximized=False):
    canvas = mplBackend.FigureCanvasSV4(chart.figure)
    manager = mplBackend.FigureManagerSV4(canvas, mplWinCount())
    w = manager.window
    w.setMinimumSize(800, 600)
    w.setWindowTitle('%s (%s)' % (chart.name, chart.sensorgroup.path))
    w.dsToolBar = ChartToolBar(w)
    w.dsToolBar.setChartCanvas(chart, canvas)
    w.mainLayout.insertWidget(0, w.dsToolBar, 0)
    if maximized:
        w.showMaximized()
    else:
        w.show()

