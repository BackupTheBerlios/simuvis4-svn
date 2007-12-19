# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QTimer
from UI.DSChartMplToolBar import Ui_DSChartMplToolBar

mplBackend = SimuVis4.Globals.plugInManager['MatPlot'].backend_sv4agg
mplWinCount = SimuVis4.Misc.Counter(1000)



class ChartToolBar(QWidget, Ui_DSChartMplToolBar):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.timer = QTimer(self)

    def setChartCanvas(self, chart, canvas):
        self.chart = chart
        self.canvas = canvas
        # FIXME: initialize all buttons and inputs



def showChartMplWindow(chart):
    chart.figure.clf()
    canvas = mplBackend.FigureCanvasSV4(chart.figure)
    manager = mplBackend.FigureManagerSV4(canvas, mplWinCount())
    manager.window.dsToolBar = ChartToolBar(manager.window)
    manager.window.dsToolBar.setChartCanvas(chart, canvas)
    manager.window.mainLayout.insertWidget(0, manager.window.dsToolBar, 0)
    chart.setTimeslice(100*86400)
    chart.makePlot(starttime=chart.sensorgroup.start)
    canvas.draw()
    manager.window.show()
