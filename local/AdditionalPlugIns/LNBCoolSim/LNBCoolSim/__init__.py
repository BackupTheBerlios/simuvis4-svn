# encoding: latin-1
# version:  $Id: __init__.py,v 1.4 2007/04/23 08:57:39 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""LNBCoolSim PlugIn for SimuVis4 """

myname = "LNBCoolSim"
proxy = None

import SimuVis4.Globals
logger = SimuVis4.Globals.logger

BuildingData = None
BuildingTypes = None
ProjectFile = None
Main = None
mainMenu = None

#from PyQt4.QtGui import QAction, QIcon, QMenu
#from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject


def plugInInit(p):
    # macht selber noch nicht viel, Initialisierung erfolgt per SimuVis-Skript!
    global proxy, BuildingData, BuildingTypes, ProjectFile, Main, mainMenu
    proxy = p
    import BuildingData, BuildingTypes, ProjectFile, Main
    mainMenu = Main.makeMenu()
    SimuVis4.Globals.mainWin.plugInMenu.addMenu(mainMenu)



def plugInExitOk():
    return True


def plugInExit(fast):
    global mainMenu
    if mainMenu is not None:
        del mainMenu
        mainMenu = None
    # FIXME: more cleanup
