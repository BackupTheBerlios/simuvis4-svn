# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""TextEditor PlugIn for SimuVis4 - provides simple text editing"""

import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn


class PlugIn(SimplePlugIn):

    def load(self):
        import Widgets, Quantities
        self.Widgets = Widgets
        self.Quantities = Quantities

    def test():
        ws = SimuVis4.Globals.mainWin.workSpace
        win = self.Widgets.TimeSignalWindow(ws)
        ws.addWindow(win)
        def printVal(val):
            print val, '|',
        win.timeSignalWidget.functions.append(printVal)
        win.show()
