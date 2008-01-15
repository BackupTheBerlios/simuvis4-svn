# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
from PyQt4.QtGui import QPen
from PyQt4.QtCore import Qt, QRectF
from PyQt4.Qwt5 import QwtPlotCurve, QwtArrayData
from numpy import array, arange


class MaskedData(QwtArrayData):
    """QwtArrayData for use with numpy.ma.MaskedArray
        from http://pyqwt.sourceforge.net/examples/MaskedDataDemo.py.html
        with some minor changes"""

    def __init__(self, x, y):
        yy = y.filled(0.0)
        QwtArrayData.__init__(self, x, yy)
        self.__mask = -y.mask
        self.__x = x
        self.__y = y

    def copy(self):
        return self

    def mask(self):
        return self.__mask

    def boundingRect(self):
        """Return the bounding rectangle of the data, accounting for the mask."""
        xmax = self.__x[self.__mask].max()
        xmin = self.__x[self.__mask].min()
        ymax = self.__y[self.__mask].max()
        ymin = self.__y[self.__mask].min()

        return QRectF(xmin, ymin, xmax-xmin, ymax-ymin)



class MaskedCurve(QwtPlotCurve):
    """QwtPlotCurve for use with numpy.ma.MaskedArray
        from http://pyqwt.sourceforge.net/examples/MaskedDataDemo.py.html
        with some minor changes"""

    def __init__(self, name=''):
        QwtPlotCurve.__init__(self, name)

    def setData(self, x, y):
        QwtPlotCurve.setData(self, MaskedData(x, y))

    def draw(self, painter, xMap, yMap, rect):
        # When the array indices contains the indices of all valid data points,
        # a chunks of valid data is indexed by
        # indices[first], indices[first+1], .., indices[last].
        # The first index of a chunk of valid data is calculated by:
        # 1. indices[i] - indices[i-1] > 1
        # 2. indices[0] is always OK
        # The last index of a chunk of valid data is calculated by:
        # 1. index[i] - index[i+1] < -1
        # 2. index[-1] is always OK
        indices = arange(self.data().size())[self.data().mask()]
        fs = array(indices)
        fs[1:] -= indices[:-1]
        fs[0] = 2
        fs = indices[fs > 1]
        ls = array(indices)
        ls[:-1] -= indices[1:]
        ls[-1] = -2
        ls = indices[ls < -1]
        for first, last in zip(fs, ls):
            QwtPlotCurve.drawFromTo(self, painter, xMap, yMap, first, last)



def showQwtPlotWindow(n, maximized=False):
    w = SimuVis4.Globals.mainWin.plugInManager['QwtPlot'].winManager.newWindow(n.path)
    if maximized:
        w.showMaximized()

    #curve = QwtPlotCurve(n.name)
    #curve.setData(n.timegrid.getTimeArray(), n[:].filled(0.0))
    curve = MaskedCurve(n.name)
    curve.setData(n.timegrid.getTimeArray(), n[:])

    curve.setPen(QPen(Qt.blue))
    curve.attach(w.plot)
    w.setMinimumSize(800, 600)
    w.plot.replot()
    w.plot.zoomer.setZoomBase()
