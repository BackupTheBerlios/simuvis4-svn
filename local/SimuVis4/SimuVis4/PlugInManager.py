# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""PlugInManager - managing SimuVis plugIns"""


import zipfile, os
from sets import Set
import Globals, PlugInProxy, Errors
from PyQt4.QtCore import QCoreApplication

logger = Globals.logger

skipFolder = ('CVS', '.svn', '.devel', 'test')


def filterPlugInList(pl):
    """ return a list of plugins sorted to fulfill all dependencies"""
    # first throw out all plugins with unfulfilled dependencies
    prov = Set()
    [prov.update(Set(p.provides)) for p in pl]
    for p in pl:
        req = Set(p.requires)
        if not req.issubset(prov):
            for miss in req.difference(prov):
                logger.warning(unicode(QCoreApplication.translate('PlugInManager',
                            'PlugInManager: plugin "%s" needs "%s" which is not provided, skipping')), p.name, miss)
            pl.remove(p)
    # then sort list roughly by amount of requirements
    pl.sort(lambda a,b: cmp(len(b.requires), len(a.requires)))
    # and finally put all elements in a new list
    new = []
    oldLen = len(pl)+1
    while pl and len(pl) < oldLen:
        oldLen = len(pl)
        p = pl.pop()
        if not new:
            new.append(p)
        else:
            found = False
            requires = Set(p.requires)
            for i in range(len(new)+1):
                provides = Set()
                [provides.update(Set(x.provides)) for x in new[:i]]
                if requires.issubset(provides):
                    found = True
                    new.insert(i, p)
                    break
            if not found:
                pl.insert(0, p)
    for p in pl:
        logger.warning(unicode(QCoreApplication.translate('PlugInManager',
                            'PlugInManager: plugin "%s" depends on broken plugins, skipping')), p.name)
    return new


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
        plist = filterPlugInList(self.plugIns.values())
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
        return None

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

    def __getitem__(self, name):
        return self.getPlugIn(name)
