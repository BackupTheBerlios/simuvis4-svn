# encoding: latin-1
# version:  $Id: __init__.py,v 1.4 2007/11/07 16:13:24 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""LNBCoolSim PlugIn for SimuVis4 """

myname = "DataBrowser"
proxy = None
browser = None

import SimuVis4
logger = SimuVis4.Globals.logger

from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QCoreApplication, Qt

cfg = SimuVis4.Globals.config
cfgsec = 'databrowser'

def configInit():
    """check if plugin config section is available, initialize if not"""
    if not cfg.has_section(cfgsec):
        cfg.add_section(cfgsec)
        cfg.set_def(cfgsec, 'show', 'yes')

def plugInInit(p):
    global proxy, browser
    proxy = p
    configInit()
    import Browser
    browser = Browser.Browser()
    SimuVis4.Globals.dataBrowser = browser
    SimuVis4.Globals.mainWin.addDockWidget(Qt.LeftDockWidgetArea, browser)
    toggleAction = browser.toggleViewAction()
    toggleAction.setShortcut(QCoreApplication.translate('DataBrowser', "Ctrl+B"))
    SimuVis4.Globals.mainWin.plugInMenu.addAction(toggleAction)
    if not cfg.getboolean(cfgsec, 'show'):
        browser.hide()
    browser.fileSystemBrowser = Browser.FileSystemBrowser()
    browser.toolBox.addItem(browser.fileSystemBrowser, QCoreApplication.translate('DataBrowser', "Filesystem"))
    if 1: #try:
        import NetCDF3
        browser.netCDF3Browser = NetCDF3.NetCDF3Browser()
        browser.toolBox.addItem(browser.netCDF3Browser, 'netCDF 3')
        #browser.netCDF3Browser.model.addNcFile('/net/Homes/joerg/blafasel.nc')
        #browser.netCDF3Browser.model.addNcFile('/net/Homes/joerg/blafasel.nc')
    else: #except:
        pass

def plugInExitOk():
    return True


def plugInExit(fast):
    pass
