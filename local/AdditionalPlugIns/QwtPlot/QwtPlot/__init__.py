# encoding: utf-8
# version:  $Id: __init__.py 67 2007-11-17 18:25:01Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""QwtPlot PlugIn for SimuVis4 - provides support classes for Qwt"""


import os
import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn
from SimuVis4.SubWinManager import SubWinManager
from PyQt4.QtGui import QAction, QIcon, QWidget, QMenu, QFileDialog, QMessageBox
from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject, QTimer


class PlugIn(SimplePlugIn):

    def load(self):
        self.initTranslations()
        cfg = SimuVis4.Globals.config
        cfgsec = self.name.lower()
        if not cfg.has_section(cfgsec):
            cfg.add_section(cfgsec)
        glb = SimuVis4.Globals
        #FIXME: this is a placeholder only...
        1/0
