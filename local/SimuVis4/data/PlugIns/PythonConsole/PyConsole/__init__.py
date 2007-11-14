# encoding: latin-1
# version:  $Id: __init__.py,v 1.4 2007/04/21 17:29:54 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""PythonConsole is a SimuVis4 plugin to get a python console with PyCute"""

import SimuVis4, os, sys
from SimuVis4.PlugIn import SimplePlugIn
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class PlugIn(SimplePlugIn):

    def load(self):
        cfg = SimuVis4.Globals.config
        cfgsec = self.name.lower()
        if not cfg.has_section(cfgsec):
            cfg.add_section(cfgsec)
            cfg.set_def(cfgsec, 'show_window', 'no')
            cfg.set_def(cfgsec, 'show_minimized', 'no')
            cfg.set_def(cfgsec, 'show_maximized', 'yes')
            cfg.set_def(cfgsec, 'use_history', 'yes')
        glb = SimuVis4.Globals
        from PyConsoleWindow import PyConsoleWindow
        self.consoleWindow = PyConsoleWindow(glb.mainWin.workSpace)
        glb.mainWin.workSpace.addWindow(self.consoleWindow)
        histF = None
        if cfg.getboolean(cfgsec, 'use_history'):
            histF = os.path.join(glb.homePath, '.SV4PyCon.his')
        self.consoleWindow.console.initInterpreter(loc=glb.__dict__, historyFile=histF)
        xpm = QPixmap()
        xpm.loadFromData(self.getFile('pycon.xpm').read())
        icon = QIcon(xpm)
        self.consoleWindow.setWindowIcon(icon)
        self.consoleWindow.setWindowTitle(QCoreApplication.translate('PyConsoleWindow', 'Python console'))
        self.consoleWindow.toggleVisibleAction.setIcon(icon)
        glb.mainWin.plugInMenu.addAction(self.consoleWindow.toggleVisibleAction)
        if cfg.getboolean(cfgsec, 'show_window'):
            if cfg.getboolean(cfgsec, 'show_maximized'):
                self.consoleWindow.showMaximized()
            elif cfg.getboolean(cfgsec, 'show_minimized'):
                self.consoleWindow.showMinimized()
            else:
                self.consoleWindow.show()


    def unload(self, fast):
        if self.consoleWindow:
            if not fast:
                self.consoleWindow.console.exitInterpreter()
                del self.consoleWindow


    def showWindow(self):
        if self.consoleWindow:
            self.consoleWindow.show()


    def hideWindow(self):
        if self.consoleWindow:
            self.consoleWindow.hide()
