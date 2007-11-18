# encoding: utf-8
# version:  $Id: __init__.py 66 2007-11-17 18:24:26Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""execute python code in SimuVis from other programs and computers"""

import SimuVis4, os, sys
from SimuVis4.PlugIn import SimplePlugIn
from PyQt4.QtGui import QAction
from PyQt4.QtCore import QCoreApplication, QObject, SIGNAL


class PlugIn(SimplePlugIn):

    def load(self):
        cfg = SimuVis4.Globals.config
        self.tcpReceiver = None
        cfgsec = self.name.lower()
        if not cfg.has_section(cfgsec):
            cfg.add_section(cfgsec)
            cfg.set_def(cfgsec, 'start_enabled', 'yes')
            cfg.set_def(cfgsec, 'tcp_port', '12345')
            cfg.set_def(cfgsec, 'cmd_queue_size', '1')
            cfg.set_def(cfgsec, 'ip_filter', '127.0.0.1')
        glb = SimuVis4.Globals
        if cfg.has_option(cfgsec, 'tcp_port'):
            tcpPort  = cfg.getint(cfgsec, 'tcp_port')
            qSize    = cfg.getint(cfgsec, 'cmd_queue_size')
            ipFilter = cfg.get(cfgsec, 'ip_filter')
            if tcpPort:
                from Receiver import CodeReceiver
                self.receiver = CodeReceiver(tcpPort, qSize, ipFilter)
                self.toggleAction = QAction(glb.mainWin)
                self.toggleAction.setText(QCoreApplication.translate('RemoteControl', 'Remote control'))
                self.toggleAction.setCheckable(True)
                QObject.connect(self.toggleAction, SIGNAL("toggled(bool)"), self.receiver.setEnabled)
                if cfg.has_option(cfgsec, 'start_enabled'):
                    self.toggleAction.setChecked(cfg.getboolean(cfgsec, 'start_enabled'))
                glb.mainWin.plugInMenu.addAction(self.toggleAction)

    def unload(self, fast):
        if self.tcpReceiver:
            if not fast:
                self.receiver.shutdown()
                self.receiver = None

