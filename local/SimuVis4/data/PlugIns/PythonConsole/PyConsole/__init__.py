# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
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
        cfg.set_def(cfgsec, 'dockwidget', 'yes')
        cfg.set_def(cfgsec, 'show', 'no')
        cfg.set_def(cfgsec, 'show_minimized', 'no')
        cfg.set_def(cfgsec, 'show_maximized', 'yes')
        cfg.set_def(cfgsec, 'use_history', 'yes')
        glb = SimuVis4.Globals
        if cfg.getboolean(cfgsec, 'dockwidget'):
            from PyConsoleWindow import PyConsoleDockWidget
            self.consoleWindow = PyConsoleDockWidget()
            SimuVis4.Globals.mainWin.addDockWidget(Qt.BottomDockWidgetArea, self.consoleWindow)
            glb.mainWin.plugInMenu.addAction(self.consoleWindow.toggleViewAction())
            if not cfg.getboolean(cfgsec, 'show'):
                self.consoleWindow.hide()
        else:
            from PyConsoleWindow import PyConsoleWindow
            self.consoleWindow = PyConsoleWindow(glb.mainWin.workSpace)
            glb.mainWin.workSpace.addSubWindow(self.consoleWindow)
            xpm = QPixmap()
            xpm.loadFromData(self.getFile('pycon.xpm').read())
            icon = QIcon(xpm)
            self.consoleWindow.setWindowIcon(icon)
            self.consoleWindow.setWindowTitle(QCoreApplication.translate('PyConsoleWindow', 'Python console'))
            self.consoleWindow.toggleVisibleAction.setIcon(icon)
            glb.mainWin.plugInMenu.addAction(self.consoleWindow.toggleVisibleAction)
            if cfg.getboolean(cfgsec, 'show'):
                if cfg.getboolean(cfgsec, 'show_maximized'):
                    self.consoleWindow.showMaximized()
                elif cfg.getboolean(cfgsec, 'show_minimized'):
                    self.consoleWindow.showMinimized()
                else:
                    self.consoleWindow.show()
        histF = None
        if cfg.getboolean(cfgsec, 'use_history'):
            histF = os.path.join(glb.homePath, '.SV4PyCon.his')
        self.consoleWindow.console.initInterpreter(loc=glb.__dict__, historyFile=histF)


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
