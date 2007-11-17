# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""SmileKit PlugIn for SimuVis4 - useful functions for SMILE"""


import SimuVis4.Globals
from SimuVis4.PlugIn import SimplePlugIn
from PyQt4.QtGui import QAction, QIcon, QMenu
from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject


class PlugIn(SimplePlugIn):

    def load(self):
        self.initTranslations()
        import Meteo2Nc
        self.Meteo2Nc = Meteo2Nc
        self.menu = QMenu(QCoreApplication.translate('SmileKit', 'SMILE'))
        mn2ncAction = QAction(QIcon(), QCoreApplication.translate('SmileKit', 'Meteonorm weather import'), SimuVis4.Globals.mainWin)
        mn2ncAction.setStatusTip(QCoreApplication.translate('SmileKit', 'Convert Meteonorm weather files to netCDF format'))
        QObject.connect(mn2ncAction, SIGNAL("triggered()"), self.showMn2NcWindow)
        self.menu.addAction(mn2ncAction)
        SimuVis4.Globals.mainWin.plugInMenu.addMenu(self.menu)


    def showMn2NcWindow(self):
        ws = SimuVis4.Globals.mainWin.workSpace
        win = self.Meteo2Nc.Meteo2NcWindow(ws)
        ws.addWindow(win)
        win.show()


    def test(self):
        self.showMn2NcWindow()
