# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, numpy

from PyQt4.QtCore import QCoreApplication

SimTools = SimuVis4.Globals.plugInManager.getPlugIn('SimTools')
RichTypes = SimTools.RichTypes
RichTypesDialog = RichTypes.Qt4Widgets.ComplexRichTypesDialog


def editMetadata(node):
    kk = node.getMetaKeys()
    qq = []
    for k in kk:
        v = node.getMetaData(k)
        t = type(v)
        if t in (str, unicode, numpy.string_):
            qq.append(RichTypes.Text(unicode(k), v))
        elif t in (bool, numpy.bool_):
            qq.append(RichTypes.Bool(str(k), not not v))
        elif t in (int, ):
            qq.append(RichTypes.Integer(str(k), v))
        elif t in (float, ):
            qq.append(RichTypes.Float(str(k), v))
        else:
            # FIXME: other data types
            pass
    title = '%s: Metadata' % node.path
    txt = unicode(QCoreApplication.translate('DataStorageBrowser', 'Edit metadata of %s')) % node.path
    dlg = RichTypesDialog(SimuVis4.Globals.mainWin, windowTitle=title, text=txt, scrolling=True)
    dlg.addRichTypes(qq)
    if not dlg.exec_():
        return
    res = dlg.result
    md = {}
    for q in res:
        md[q.name] = q.v
    node.setMetaData(md)
    # FIXME: type conversion ?
