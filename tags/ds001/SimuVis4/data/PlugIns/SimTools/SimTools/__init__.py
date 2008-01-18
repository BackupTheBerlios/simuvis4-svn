# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn


class PlugIn(SimplePlugIn):

    def load(self):
        import Widgets
        self.Widgets = Widgets
        try:
            import RichTypes
            self.RichTypes = RichTypes
        except ImportError:
            import MyRichTypes
            self.RichTypes = MyRichTypes
        return True


    def test():
        ws = SimuVis4.Globals.mainWin.workSpace
        win = self.Widgets.TimeSignalWindow(ws)
        ws.addSubWindow(win)
        def printVal(val):
            print val, '|',
        win.timeSignalWidget.functions.append(printVal)
        win.show()
