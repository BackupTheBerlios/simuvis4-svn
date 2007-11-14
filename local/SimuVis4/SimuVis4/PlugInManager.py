# encoding: latin-1
# version:  $Id: PlugInManager.py,v 1.6 2007/11/07 16:13:24 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""PlugInManager - managing python plugIns"""


import zipfile, os
import Globals, PlugInProxy, Errors
from PyQt4.QtCore import QCoreApplication

logger = Globals.logger

skipFolder = ('CVS', '.svn')

class PlugInManager:

    def __init__(self):
        self.plugIns = {}
        self.ignoreList = Globals.config['main:ignore_plugins'].split()

    def loadSingle(self, path):
        logger.info(unicode(QCoreApplication.translate('PlugInManager', 'PlugInManager: trying to load plugin from: "%s"')), path)
        try:
            if zipfile.is_zipfile(path):
                p = PlugInProxy.PlugInZipProxy(path)
            elif os.path.isdir(path):
                p = PlugInProxy.PlugInFolderProxy(path)
            else:
                logger.error(unicode(QCoreApplication.translate('PlugInManager', 'PlugInManager: this is not a plugin: "%s"')), path)
        except:
            logger.exception(unicode(QCoreApplication.translate('PlugInManager', 'PlugInManager: broken plugin in "%s"')), path)
            return
        n = p.name
        if n in self.plugIns:
            o = self.plugIns[n]
            if p.version <= o.version:
                logger.warning(unicode(QCoreApplication.translate('PlugInManager', 'PlugInManager: plugin "%s" with same or newer version is already registered from: "%s"')), n, o.path)
                return
        if n in self.ignoreList:
            logger.warning(unicode(QCoreApplication.translate('PlugInManager', 'PlugInManager: plugin "%s" was marked to be ignored, skipping')), n)
            return
        self.plugIns[n] = p

    def loadAllFromFolder(self, path):
        [self.loadSingle(os.path.join(path, f)) for f in os.listdir(path) if not f in skipFolder]

    def initializePlugIns(self, prg=None):
        plist = self.plugIns.values()
        # FIXME: sort list o plugins to meet dependencies
        #print [(p.name, p.requires) for p in plist]
        plist.sort(cmp = lambda a,b: cmp(len(a.requires), len(b.requires)))
        #print [(p.name, p.requires) for p in plist]
        for p in plist:
            prg(unicode(QCoreApplication.translate('PlugInManager', 'Initializing plugin: %s')) % p.name)
            if p.state < 2:
                p.init()

    def hasPlugIn(self, name):
        return name in self.plugIns

    def listPlugIns(self):
        return self.plugIns.keys()

    def getPlugIn(self, name):
        p = self.plugIns[name]
        try:
            return p()
        except:
            logger.exception(unicode(QCoreApplication.translate('PlugInManager', 'PlugInManager: exception while loading the plugin: "%s"')), name)

    def getInteractive(self, name):
        try:
            return self.plugIns[name]
        except:
            raise Errors.FeatureMissingError('FIXME: ask for installation of plugIns')

    def shutdownOk(self):
        for p in self.plugIns.values():
            if p.state == 2:
                if not p.exitOk():
                    return False
        return True

    def shutdown(self):
        for p in self.plugIns.values():
            if p.state == 2:
                p.disable(False)
