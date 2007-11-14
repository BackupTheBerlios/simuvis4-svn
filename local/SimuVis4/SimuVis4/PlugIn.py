# encoding: latin-1
# version:  $Id: PlugIn.py,v 1.7 2007/11/07 16:13:24 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""PlugIn - managing python plugins"""

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


class PlugInFolder:
    """PlugIn class to hold information on a SimuVis plugin and act
    as a proxy for a plugin which is contained in an ordinary folder"""

    def __init__(self, path):
        self.state = 0
        self.cfg = {"name": "[UNKNOWN]"}
        self.file = ''
        self.proxy = None
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
        sys.path.insert(0, self.path)
        self.state = -1
        try:
            self.proxy = __import__(self.package)
            self.state = 1
            self.proxy.plugInInit(self)
            self.state = 2
            logger.info(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: successfully initialized "%s"')), self.name)
        except:
            logger.exception(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: error while initializing plugin "%s"')), self.name)
            self.state = -1
            self.proxy = None
        del sys.path[0]

    def xreload(self):
        raise Errors.FeatureMissingError('FIXME: plugin reloading')

    def __call__(self):
        if not self.proxy:
            self.init()
        if not self.proxy:
            raise Errors.PlugInError()
        return self.proxy

    def exitOk(self):
        try:
            return self.proxy.plugInExitOk()
        except AttributeError:
            return True

    def disable(self, fast=False):
        self.proxy.plugInExit(fast)
        self.state = 0


class PlugInZip(PlugInFolder):
    """Special type of PlugIn that is completely self-contained in a single zipfile"""
    
    def extraInit(self):
        self.file = zipfile.ZipFile(self.path)

    def openFile(self, path, mode='r'):
        logger.debug(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: serving file "%s" from plugin-path "%s"')), path, self.path)
        return StringIO.StringIO(self.file.read(path))
