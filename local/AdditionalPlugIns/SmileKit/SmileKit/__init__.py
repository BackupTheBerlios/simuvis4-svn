# encoding: latin-1
# version:  $Id: __init__.py,v 1.4 2007/08/13 09:16:52 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""TextEditor PlugIn for SimuVis4 - provides simple text editing"""

myname = "SmileKit"
proxy = None
menu = None
Meteo2Nc = None


import SimuVis4.Globals
logger = SimuVis4.Globals.logger

from PyQt4.QtGui import QAction, QIcon, QMenu
from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject

def plugInInit(p):
    global proxy, Meteo2Nc, menu
    proxy = p
    import Meteo2Nc

    menu = QMenu(QCoreApplication.translate('SmileKit', 'SMILE'))
    mn2ncAction = QAction(QIcon(), QCoreApplication.translate('SmileKit', 'Meteonorm weather import'), SimuVis4.Globals.mainWin)
    mn2ncAction.setStatusTip(QCoreApplication.translate('SmileKit', 'Convert Meteonrom weather files to netCDF format'))
    QObject.connect(mn2ncAction, SIGNAL("triggered()"), showMn2NcWindow)
    menu.addAction(mn2ncAction)
    SimuVis4.Globals.mainWin.plugInMenu.addMenu(menu)


def plugInExitOk():
    return True


def plugInExit(fast):
    pass


def showMn2NcWindow():
    ws = SimuVis4.Globals.mainWin.workSpace
    win = Meteo2Nc.Meteo2NcWindow(ws)
    ws.addWindow(win)
    win.show()


def test():
    showMn2NcWindow()
