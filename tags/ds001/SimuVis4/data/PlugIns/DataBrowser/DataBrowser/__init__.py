# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
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
        cfg.set_def(cfgsec, 'netcdf3_browser', 'yes')
        cfg.set_def(cfgsec, 'filesystem_browser', 'yes')
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
        if cfg.getboolean(cfgsec, 'filesystem_browser'):
            browser.fileSystemBrowser = Browser.FileSystemBrowser()
            browser.toolBox.addItem(browser.fileSystemBrowser, QCoreApplication.translate('DataBrowser', "Filesystem"))
        if cfg.getboolean(cfgsec, 'netcdf3_browser'):
            try:
                import NetCDF3
                browser.netCDF3Browser = NetCDF3.NetCDF3Browser()
                browser.toolBox.addItem(browser.netCDF3Browser, 'netCDF 3')
            except ImportError:
                SimuVis4.Globals.logger.error(unicode(QCoreApplication.translate('DataBrowser',
                    'DataBrowser: could not load browser for netCDF3')))
        return True
