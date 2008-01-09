# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QTimer, SIGNAL
from UI.DSChartMplToolBar import Ui_DSChartMplToolBar

mplBackend = SimuVis4.Globals.plugInManager['MatPlot'].backend_sv4agg
mplWinCount = SimuVis4.Misc.Counter(1000)

unitFactors = [60, 3600, 86400, 604800, 2592000, 31536000]


class ChartToolBar(QWidget, Ui_DSChartMplToolBar):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.timer = QTimer(self)
        self.LengthInput.setValue(1)
        self.LengthUnitInput.setCurrentIndex(2)
        self.connect(self.LengthInput, SIGNAL('valueChanged(int)'), self.lengthChanged)
        self.connect(self.LengthUnitInput, SIGNAL('activated(int)'), self.lengthUnitChanged)


    def setChartCanvas(self, chart, canvas):
        self.chart = chart
        self.canvas = canvas
        self.LengthInput.setValue(100)
        self.LengthUnitInput.setCurrentIndex(2)
        self.showChart()


    def lengthChanged(self, l):
        self.setTimeslice(l * unitFactors[self.LengthUnitInput.currentIndex()])


    def lengthUnitChanged(self, i):
        self.setTimeslice(unitFactors[i] * self.LengthInput.value())


    def setTimeslice(self, ts):
        if not ts == self.chart.timeslice:
            self.chart.setTimeslice(ts)
            self.showChart()


    def showChart(self, startTime=None):
        self.chart.figure.clf()
        if startTime is None:
            startTime = self.chart.sensorgroup.start
        self.chart.makePlot(startTime)
        self.canvas.draw()



def showChartMplWindow(chart):
    canvas = mplBackend.FigureCanvasSV4(chart.figure)
    manager = mplBackend.FigureManagerSV4(canvas, mplWinCount())
    manager.window.dsToolBar = ChartToolBar(manager.window)
    manager.window.dsToolBar.setChartCanvas(chart, canvas)
    manager.window.mainLayout.insertWidget(0, manager.window.dsToolBar, 0)
    manager.window.show()

