# encoding: utf-8
# version:  $Id: VtkWindow.py 67 2007-11-17 18:25:01Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""
This module will change PyQt4.Qwt5.qplt to open Plot()- and IPlot()-windows as MDI-subwindows
in SimuVis with some additional functions.
"""

import SimuVis4
from PyQt4.QtCore import QCoreApplication

try:
    import PyQt4.Qwt5.qplt
    from QwtPlotWindow import QwtPlotWindow

    _Plot = PyQt4.Qwt5.qplt.Plot

    def Plot(*args):
        win = QwtPlotWindow(SimuVis4.Globals.mainWin.workSpace, _Plot, *args)
        SimuVis4.Globals.mainWin.workSpace.addSubWindow(win)
        win.show()
        return win.plot
    PyQt4.Qwt5.qplt.Plot  = Plot
    PyQt4.Qwt5.qplt.IPlot = Plot

    SimuVis4.Globals.logger.info(QCoreApplication.translate('QwtPlot',
        'QwtPlot: support for PyQt4.Qwt5.qplt in subwindows was successfully installed'))

except ImportError:
    SimuVis4.Globals.logger.info(QCoreApplication.translate('QwtPlot',
        'QwtPlot: PyQt4.Qwt5.qplt not found, skipped subwindow support'))
