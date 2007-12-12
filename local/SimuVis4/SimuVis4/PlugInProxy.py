# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""PlugInProxy - hold connection to a real plugin"""

import os, zipfile, ConfigParser, sys
from PyQt4.QtCore import QCoreApplication
try:
    import cStringIO as StringIO
except:
    import StringIO

import Globals, Errors
logger = Globals.logger
    
metaFileName = 'PLUGIN.INI'
cfgSection = 'plugin'


class PlugInFolderProxy:
    """PlugInProxy class to hold information on a SimuVis plugin and act
    as a proxy for a plugin which is contained in an ordinary folder"""

    def __init__(self, path):
        self.state = 0
        self.cfg = {"name": "[UNKNOWN]"}
        self.file = ''
        self.plugIn = None
        self.path = os.path.abspath(path)
        self.extraInit()
        cp = cfg = ConfigParser.ConfigParser()
        cp.readfp(self.openFile(metaFileName))
        self.name       = cp.get(cfgSection, 'name')
        self.package    = cp.get(cfgSection, 'package')
        self.version    = cp.get(cfgSection, 'version')
        self.description= cp.get(cfgSection, 'description')
        self.requires   = cp.get(cfgSection, 'requires').split()
        self.provides   = cp.get(cfgSection, 'provides').split()
        # FIXME: get more!

    def extraInit(self):
        pass

    def openFile(self, path, mode='r'):
        logger.debug(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: serving file "%s" from plugin-path "%s"')), path, self.path)
        return open(os.path.join(self.path, path), mode)

    def init(self):
        if self.state != 0:
            return
        sys.path.insert(0, self.path)
        try:
            m = __import__(self.package)
            self.state = 1
            self.plugIn = m.PlugIn(self, self.name)
            self.state = 2
            logger.info(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: %s: successfully initialized')), self.name)
        except:
            logger.error(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: %s: error while initializing plugin')), self.name)
            self.state = 3
            self.plugIn = None
        del sys.path[0]

    def xreload(self):
        raise Errors.FeatureMissingError('FIXME: plugin reloading')

    def __call__(self):
        if not self.plugIn:
            self.init()
        if not self.plugIn:
            raise Errors.PlugInError()
        return self.plugIn

    def exitOk(self):
        try:
            return self.plugIn.exitOk()
        except AttributeError:
            return True

    def disable(self, fast=False):
        self.plugIn.doExit(fast)
        self.state = 0


class PlugInZipProxy(PlugInFolderProxy):
    """Special type of PlugIn that is completely self-contained in a single zipfile"""
    
    def extraInit(self):
        self.file = zipfile.ZipFile(self.path)

    def openFile(self, path, mode='r'):
        logger.debug(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: serving file "%s" from plugin-path "%s"')), path, self.path)
        return StringIO.StringIO(self.file.read(path))
