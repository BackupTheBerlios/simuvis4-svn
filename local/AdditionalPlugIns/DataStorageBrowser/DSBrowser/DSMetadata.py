# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, numpy
SimTools = SimuVis4.Globals.plugInManager.getPlugIn('SimTools')
Quantities = SimTools.Quantities
#QuantitiesDialog = SimTools.Widgets.SimpleQuantitiesDialog
QuantitiesDialog = SimTools.Widgets.ComplexQuantitiesDialog


def addMetadata(node):
    pass


def editMetadata(node):
    kk = node.getMetaKeys()
    qq = []
    for k in kk:
        v = node.getMetaData(k)
        t = type(v)
        if t == numpy.string_:
            qq.append(Quantities.Text(str(k), v))
        elif t == numpy.bool_:
            qq.append(Quantities.Bool(str(k), not not v))
        else:
            # FIXME: other data types
            pass
    title = '%s: Metadata' % node.path
    txt = 'Edit metadata of %s' % node.path
    dlg = QuantitiesDialog(SimuVis4.Globals.mainWin, windowTitle=title, text=txt, scrolling=True)
    dlg.addQuantities(qq)
    dlg.exec_()
    res = dlg.result
    #md = {}
    #for q in res:
    #    md[q.name] = q.v
    #node.setMetaData(md)
    # FIXME: type conversion, delete metadata ... ?
    