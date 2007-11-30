# encoding: utf-8
# version:  $Id: __init__.py 67 2007-11-17 18:25:01Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""QwtPlot PlugIn for SimuVis4 - provides support classes for Qwt"""


import os
import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn
from SimuVis4.SubWinManager import SubWinManager
from PyQt4.QtGui import QAction, QIcon, QWidget, QMenu, QFileDialog, QMessageBox, QPixmap
from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject, QTimer


class PlugIn(SimplePlugIn):

    def load(self):
        self.initTranslations()
        cfg = SimuVis4.Globals.config
        cfgsec = self.name.lower()
        if not cfg.has_section(cfgsec):
            cfg.add_section(cfgsec)
        glb = SimuVis4.Globals
        import QwtPlotWindow, QPlot
        self.QwtPlotWindow = QwtPlotWindow
        xpm = QPixmap()
        xpm.loadFromData(self.getFile('plotwin.xpm').read())
        winIcon = QIcon(xpm)
        self.winManager = SubWinManager(SimuVis4.Globals.mainWin.workSpace, QwtPlotWindow.QwtPlotWindow,
                QCoreApplication.translate('QwtPlot', 'Qwt Plotwindow'), winIcon)
        testAction = QAction(winIcon,
            QCoreApplication.translate('QwtPlot', '&QwtPlotWindow Test'), SimuVis4.Globals.mainWin)
        testAction.setStatusTip(QCoreApplication.translate('QwtPlot', 'Show a new Qwt test window'))
        QWidget.connect(testAction, SIGNAL("triggered()"), self.test)
        SimuVis4.Globals.mainWin.plugInMenu.addAction(testAction)

    def test(self):
        from math import sin, cos
        from PyQt4.Qwt5 import QwtPlotCurve
        w = self.winManager.newWindow()
        plt = w.plot
        xx = [0.05*x for x in range(100)]
        y1 = [sin(x) for x in xx]
        y2 = [cos(x) for x in xx]
        curve1 = QwtPlotCurve('sin(x)')
        curve1.attach(plt)
        curve1.setData(xx, y1)
        curve2 = QwtPlotCurve('cos(x)')
        curve2.attach(plt)
        curve2.setData(xx, y2)
