# encoding: latin-1
# version:  $Id: __init__.py,v 1.4 2007/04/21 17:30:44 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""TextEditor PlugIn for SimuVis4 - provides simple text editing"""

myname = "SimTools"
proxy = None
Widgets = None
Quantities = None

import SimuVis4.Globals
logger = SimuVis4.Globals.logger


def plugInInit(p):
    global proxy, Widgets
    proxy = p
    import Widgets, Quantities


def plugInExitOk():
    return True


def plugInExit(fast):
    pass


def test():
    ws = SimuVis4.Globals.mainWin.workSpace
    win = Widgets.TimeSignalWindow(ws)
    ws.addWindow(win)
    def printVal(val):
        print val, '|',
    win.timeSignalWidget.functions.append(printVal)
    win.show()
