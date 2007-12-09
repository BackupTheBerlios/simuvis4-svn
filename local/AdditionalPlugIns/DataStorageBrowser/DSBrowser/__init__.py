# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""LNBCoolSim PlugIn for SimuVis4 """

import sys
import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QCoreApplication, Qt

class PlugIn(SimplePlugIn):

    def load(self):
        self.initTranslations()
        cfg = SimuVis4.Globals.config
        cfgsec = self.name.lower()
        if not cfg.has_section(cfgsec):
            cfg.add_section(cfgsec)
        # cfg.set_def(cfgsec, 'datastorage_path', '/net/Dezentral/Projekte/Angebote/ISE_DataStorage-GUI/nmd/')
        # cfg.set_def(cfgsec, 'default_database', '/net/Dezentral/Projekte/Angebote/ISE_DataStorage-GUI/nmd/datastorage/wetter')
        if cfg.has_option(cfgsec, 'datastorage_path'):
            sys.path.append(cfg.get(cfgsec, 'datastorage_path'))
        try:
            import DSBrowser
            dsbrowser = DSBrowser.DSBrowser()
            SimuVis4.Globals.dataBrowser.toolBox.addItem(dsbrowser, 'DataStorage')
            if cfg.has_option(cfgsec, 'default_database'):
                dsbrowser.loadDatabase(cfg.get(cfgsec, 'default_database'))
        except ImportError:
            SimuVis4.Globals.logger.error(unicode(QCoreApplication.translate('DataStorageBrowser',
                'DataStorageBrowser: could not load module datastorage, check paths!')))
