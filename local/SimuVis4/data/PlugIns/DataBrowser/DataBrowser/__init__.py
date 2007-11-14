# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""LNBCoolSim PlugIn for SimuVis4 """

import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QCoreApplication, Qt

class PlugIn(SimplePlugIn):

    def load(self):
        cfg = SimuVis4.Globals.config
        cfgsec = self.name.lower()
        if not cfg.has_section(cfgsec):
            cfg.add_section(cfgsec)
            cfg.set_def(cfgsec, 'show', 'yes')
        glb = SimuVis4.Globals
        import Browser
        browser = Browser.Browser()
        glb.dataBrowser = browser
        glb.mainWin.addDockWidget(Qt.LeftDockWidgetArea, browser)
        toggleAction = browser.toggleViewAction()
        toggleAction.setShortcut(QCoreApplication.translate('DataBrowser', "Ctrl+B"))
        glb.mainWin.plugInMenu.addAction(toggleAction)
        if not cfg.getboolean(cfgsec, 'show'):
            browser.hide()
        browser.fileSystemBrowser = Browser.FileSystemBrowser()
        browser.toolBox.addItem(browser.fileSystemBrowser, QCoreApplication.translate('DataBrowser', "Filesystem"))
        try:
            import NetCDF3
            browser.netCDF3Browser = NetCDF3.NetCDF3Browser()
            browser.toolBox.addItem(browser.netCDF3Browser, 'netCDF 3')
            #browser.netCDF3Browser.model.addNcFile('/net/Homes/joerg/blafasel.nc')
        except:
            pass
