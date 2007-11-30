# encoding: utf-8
# version:  $Id: VtkWindow.py 67 2007-11-17 18:25:01Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
import PyQt4.Qwt5.qplt
import QwtWindow

_Plot = PyQt4.Qwt5.qplt.Plot

def Plot(*args):
    win = QwtWindow.QwtPlotWindow(SimuVis4.Globals.mainWin.workSpace, _Plot, *args)
    SimuVis4.Globals.mainWin.workSpace.addSubWindow(win)
    win.show()

PyQt4.Qwt5.qplt.Plot = Plot
