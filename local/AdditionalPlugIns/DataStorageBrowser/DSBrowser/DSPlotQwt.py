# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
from PyQt4.QtGui import QPen
from PyQt4.QtCore import Qt
from PyQt4.Qwt5 import QwtPlotCurve


def showQwtPlotWindow(n, maximized=False):
    w = SimuVis4.Globals.mainWin.plugInManager['QwtPlot'].winManager.newWindow(n.path)
    if maximized:
        w.showMaximized()
    curve = QwtPlotCurve(n.name)
    curve.setData(n.timegrid.getTimeArray(), n[:].filled(0.0))
    curve.setPen(QPen(Qt.blue))
    curve.attach(w.plot)
    w.setMinimumSize(800, 600)
    w.plot.replot()
    w.plot.zoomer.setZoomBase()