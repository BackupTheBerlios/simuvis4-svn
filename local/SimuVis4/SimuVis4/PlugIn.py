# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
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
        self.load()
        self._loaded = True


    def initTranslations(self):
        if self._glb.language:
            if 1: #try:
                self._translator = QTranslator()
                self._translator.load(self.getFile('%s.qm' % self._glb.language).read())
                self._glb.application.installTranslator(self._translator)
            else: #except:
                self._glb.logger.info(unicode(QCoreApplication.translate('PlugIn', '%s: could not load translations for language "%s", skipping')),
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
