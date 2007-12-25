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
        self.receiver = None
        cfgsec = self.name.lower()
        if not cfg.has_section(cfgsec):
            cfg.add_section(cfgsec)
        cfg.set_def(cfgsec, 'start_enabled', 'yes')
        cfg.set_def(cfgsec, 'tcp_port', '12345')
        cfg.set_def(cfgsec, 'ip_filter', '127.0.0.1')
        cfg.set_def(cfgsec, 'raise_mainwindow', 'yes')
        cfg.set_def(cfgsec, 'raise_use_hack', 'no')
        glb = SimuVis4.Globals
        tcpPort  = cfg.getint(cfgsec, 'tcp_port')
        qSize    = cfg.getint(cfgsec, 'cmd_queue_size')
        ipFilter = cfg.get(cfgsec, 'ip_filter')
        from Receiver import CodeReceiver
        self.receiver = CodeReceiver(tcpPort, ipFilter, cfg.getboolean(cfgsec, 'raise_mainwindow'),
            cfg.getboolean(cfgsec, 'raise_use_hack'))
        if not self.receiver.isListening():
            SimuVis4.Globals.logger.exception(unicode(QCoreApplication.translate('RemoteControl',
                'RemoteControl: could not start TCP listener at port %s')), tcpPort)
        self.toggleAction = QAction(glb.mainWin)
        self.toggleAction.setText(QCoreApplication.translate('RemoteControl', 'Remote control active'))
        self.toggleAction.setCheckable(True)
        QObject.connect(self.toggleAction, SIGNAL("toggled(bool)"), self.receiver.setEnabled)
        if cfg.has_option(cfgsec, 'start_enabled'):
            self.toggleAction.setChecked(cfg.getboolean(cfgsec, 'start_enabled'))
        glb.mainWin.plugInMenu.addAction(self.toggleAction)
        return True        
                

    def unload(self, fast):
        if self.receiver:
            del self.receiver
            self.receiver = None
