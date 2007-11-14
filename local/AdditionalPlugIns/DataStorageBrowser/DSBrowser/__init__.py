# encoding: latin-1
# version:  $Id: __init__.py,v 1.1 2007/11/07 16:13:24 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""LNBCoolSim PlugIn for SimuVis4 """

myname = "DataStorageBrowser"
proxy = None
browser = None

import sys
import SimuVis4 #, SimuVis4.Globals
logger = SimuVis4.Globals.logger

from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QCoreApplication, Qt

cfg = SimuVis4.Globals.config
cfgsec = 'dsbrowser'


def configInit():
    """check if plugin config section is available, initialize if not"""
    if not cfg.has_section(cfgsec):
        cfg.add_section(cfgsec)
        cfg.set_def(cfgsec, 'datastorage_path', '/net/Dezentral/Projekte/Angebote/ISE_DataStorage-GUI/nmd/')
        cfg.set_def(cfgsec, 'default_database', '/net/Dezentral/Projekte/Angebote/ISE_DataStorage-GUI/nmd/datastorage/wetter')


def plugInInit(p):
    global proxy, browser
    proxy = p
    configInit()
    sys.path.append(cfg.get(cfgsec, 'datastorage_path'))
    import DSBrowser
    dsbrowser = DSBrowser.DSBrowser()
    SimuVis4.Globals.dataBrowser.toolBox.addItem(dsbrowser, 'DataStorage')
    dsbrowser.model.addDatabase(cfg.get(cfgsec, 'default_database'))


def plugInExitOk():
    return True


def plugInExit(fast):
    SimuVis4.Globals.dataBrowser = None
    pass
