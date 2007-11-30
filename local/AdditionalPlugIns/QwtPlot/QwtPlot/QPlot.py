# encoding: utf-8
# version:  $Id: VtkWindow.py 67 2007-11-17 18:25:01Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""
This module will change PyQt4.Qwt5.qplt to open Plot()-windows as MDI-subwindows
in SimuVis with some additional functions.
"""

import SimuVis4
import PyQt4.Qwt5.qplt
from QwtPlotWindow import QwtPlotWindow

_Plot = PyQt4.Qwt5.qplt.Plot

def Plot(*args):
    win = QwtPlotWindow(SimuVis4.Globals.mainWin.workSpace, _Plot, *args)
    SimuVis4.Globals.mainWin.workSpace.addSubWindow(win)
    win.show()

PyQt4.Qwt5.qplt.Plot = Plot