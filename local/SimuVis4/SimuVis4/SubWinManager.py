# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4.Misc

class SubWinManager(object):

    def __init__(self, workSpace, subWinClass, winName, winIcon):
        self.workSpace = workSpace
        self.subWinClass = subWinClass
        self.winName = winName
        self.winIcon = winIcon
        self.counter = SimuVis4.Misc.Counter(1)
        self.windows = []

    def getActiveWindow(self):
        w = self.workSpace.activeSubWindow()
        if not w in self.windows:
            return None
        return w

    def shutdown(self):
        for w in self.windows:
            w.close()

    def newWindow(self, name=None):
        if not name:
            name = "%s %d" % (self.winName, self.counter())
        w = self.subWinClass(self.workSpace)
        self.workSpace.addSubWindow(w)
        self.windows.append(w)
        w.setWindowIcon(self.winIcon)
        w.setWindowTitle(name)
        w.show()
        return w

    def closeWindow(self, w=None):
        if not w:
            w = self.getActiveWindow()
        if w:
            w.close()
