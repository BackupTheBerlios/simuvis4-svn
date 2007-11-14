# encoding: latin-1
# version:  $Id: __init__.py,v 1.4 2007/04/21 17:29:54 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""PythonConsole is a SimuVis4 plugin to get a python console with PyCute"""

import os, sys
import SimuVis4.Globals as Globals
from PyQt4.QtGui import *
from PyQt4.QtCore import *

myname = "PythonConsole"

cfg = Globals.config
cfgsec = 'python_console'

proxy  = None
consoleWindow = None


def configInit():
    """check if plugin config section is available, initialize if not"""
    if not cfg.has_section(cfgsec):
        cfg.add_section(cfgsec)
        cfg.set_def(cfgsec, 'show_window', 'no')
        cfg.set_def(cfgsec, 'show_minimized', 'no')
        cfg.set_def(cfgsec, 'show_maximized', 'yes')
        cfg.set_def(cfgsec, 'use_history', 'yes')


def plugInInit(p):
    global proxy, consoleWindow
    proxy = p
    configInit()
    from PyConsoleWindow import PyConsoleWindow
    consoleWindow = PyConsoleWindow(Globals.mainWin.workSpace)
    Globals.mainWin.workSpace.addWindow(consoleWindow)
    histF = None
    if cfg.getboolean(cfgsec, 'use_history'):
        histF = os.path.join(Globals.homePath, '.SV4PyCon.his')
    consoleWindow.console.initInterpreter(loc=Globals.__dict__, historyFile=histF)
    xpm = QPixmap()
    xpm.loadFromData(proxy.openFile('pycon.xpm').read())
    icon = QIcon(xpm)
    consoleWindow.setWindowIcon(icon)
    consoleWindow.setWindowTitle(QCoreApplication.translate('PyConsoleWindow', 'Python console'))
    consoleWindow.toggleVisibleAction.setIcon(icon)
    Globals.mainWin.plugInMenu.addAction(consoleWindow.toggleVisibleAction)
    if cfg.getboolean(cfgsec, 'show_window'):
        if cfg.getboolean(cfgsec, 'show_maximized'):
            consoleWindow.showMaximized()
        elif cfg.getboolean(cfgsec, 'show_minimized'):
            consoleWindow.showMinimized()
        else:
            consoleWindow.show()


def plugInExitOk():
    return True

    
def plugInExit(fast):
    global consoleWindow
    if consoleWindow:
        if not fast:
            consoleWindow.console.exitInterpreter()
            del consoleWindow

            
def showWindow():
    if consoleWindow:
        consoleWindow.show()

        
def hideWindow():
    if consoleWindow:
        consoleWindow.hide()
