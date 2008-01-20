# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
from PyQt4.QtGui import QPen
from PyQt4.QtCore import Qt, QRectF
from numpy import array, arange

QwtPlot = SimuVis4.Globals.plugInManager.getPlugIn('QwtPlot')
MaskedCurve = QwtPlot.MaskedArray.MaskedCurve


def showQwtPlotWindow(n, maximized=False):
    w = SimuVis4.Globals.mainWin.plugInManager['QwtPlot'].winManager.newWindow(n.path)
    if maximized:
        w.showMaximized()

    curve = MaskedCurve(n.name)
    curve.setData(n.timegrid.getTimeArray(), n[:])

    curve.setPen(QPen(Qt.blue))
    curve.attach(w.plot)
    w.setMinimumSize(640, 480)
    w.plot.replot()
    w.plot.zoomer.setZoomBase()
