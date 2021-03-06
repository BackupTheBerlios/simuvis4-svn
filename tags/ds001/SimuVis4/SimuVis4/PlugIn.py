# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""PlugIn - managing SimuVis4 plugins"""

import SimuVis4
from PyQt4.QtCore import QCoreApplication, QTranslator

class SimplePlugIn:
    """PluginClass to be used INSIDE the PlugIn modules"""

    def __init__(self, proxy, name):
        self._proxy = proxy
        self._glb = SimuVis4.Globals
        self._translator = None
        self._loaded = False
        self.name = name
        self._loaded = self.load()
        if not self._loaded:
            raise SimuVis4.Errors.PlugInError()


    def initTranslations(self):
        if self._glb.language and self._glb.language != 'en':
            try:
                self._translator = QTranslator()
                self._qm = self.getFile('%s.qm' % self._glb.language).read()
                self._translator.loadFromData(self._qm)
                self._glb.application.installTranslator(self._translator)
                self._glb.logger.debug(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: %s: translation loaded for language "%s"')),
                    self.name, self._glb.language)
            except:
                self._glb.logger.warning(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: %s: could not load translations for language "%s", skipping')),
                    self.name, self._glb.language)
                self._translator = None


    def getFile(self, fileName):
        return self._proxy.openFile(fileName)


    def doExit(self, fast=False):
        if not self._loaded:
            return
        if not fast:
            if self._translator:
                SimuVis4.Globals.application.removeTranslator(self._translator)
        self._glb.logger.info(unicode(QCoreApplication.translate('PlugIn', 'PlugIn: %s: trying to unload')), self.name)
        self.unload(fast)


    def test(self):
        # overload me!
        pass


    def exitOk(self):
        # overload me!
        return True


    def load(self):
        # overload me!
        pass


    def unload(self, fast):
        # overload me!
        pass
