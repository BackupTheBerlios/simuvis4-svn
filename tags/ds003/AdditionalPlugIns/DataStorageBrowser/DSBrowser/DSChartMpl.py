# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, Icons, os
from PyQt4.QtGui import QWidget, QIcon, QPixmap, QFileDialog
from PyQt4.QtCore import QTimer, SIGNAL, QDateTime, QCoreApplication
from UI.DSChartMplToolBar import Ui_DSChartMplToolBar

mplBackend = SimuVis4.Globals.plugInManager['MatPlot'].backend_sv4agg
mplWinCount = SimuVis4.Misc.Counter(1000)

unitFactors = [60, 3600, 86400, 604800, 2592000, 31536000]

showOriginalSize = SimuVis4.Globals.config.getboolean('datastoragebrowser', 'show_chart_original_size')


class ChartToolBar(QWidget, Ui_DSChartMplToolBar):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
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
        slc = chart.standardSlice
        self.startTime = chart.sensorgroup.stop - slc
        dt = QDateTime()
        dt.setTime_t(self.startTime)
        self.StartInput.setDateTime(dt)
        mindt = QDateTime()
        mindt.setTime_t(chart.sensorgroup.start)
        self.StartInput.setMinimumDate(mindt.date())
        # try to guess unit*factor from slice
        uF = unitFactors[:]
        uF.reverse()
        for f in uF:
            if not slc % f:
                self.LengthUnitInput.setCurrentIndex(unitFactors.index(f))
                self.LengthInput.setValue(slc / f)
                self.setTimeslice(slc)
                break
        else:
            self.LengthInput.setValue(1)
            self.LengthUnitInput.setCurrentIndex(3)
            self.setTimeslice(unitFactors[3])
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
    w.setMinimumSize(640, 480)
    w.setWindowTitle('%s (%s)' % (chart.name, chart.sensorgroup.path))
    w.dsToolBar = ChartToolBar(w)
    w.dsToolBar.setChartCanvas(chart, canvas)
    w.mainLayout.insertWidget(0, w.dsToolBar, 0)
    if showOriginalSize and chart.options['size']:
        w.toolbar.wheelButton.setChecked(True)
        x, y = chart.options['size']
        w.canvas.resize(x, y)
    if maximized:
        w.showMaximized()
    else:
        w.show()


def saveAllChartImages(sg):
    # FIXME: this gives an error - why?
    f = QFileDialog.getExistingDirectory(SimuVis4.Globals.mainWin,
        QCoreApplication.translate('DataStorageBrowser',
        "Select a folder (existing image files will be overwritten!)"),
        SimuVis4.Globals.defaultFolder)
    if f.isEmpty():
        return
    folder = unicode(f)
    SimuVis4.Globals.defaultFolder = folder
    for chart in sg.charts.values():
        fileName = "%s.png" % chart.name
        chart.setTimeslice(1*86400)
        chart(starttime=sg.start, filename=os.path.join(folder, fileName))
