# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""MatPlot PlugIn for SimuVis4 - provides an interface to matplotlib/pylab"""


import os
import SimuVis4
from SimuVis4.PlugIn import SimplePlugIn
from SimuVis4.SubWinManager import SubWinManager
from PyQt4.QtGui import QAction, QIcon, QWidget, QMenu, QFileDialog, QMessageBox
from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject, QTimer


configWarningText = unicode(QCoreApplication.translate('MatPlot',
"""The MatPlot plugin enables matplotlib/pylab to be
used from within SimuVis4. Unfortinately some manual
intervention is necessary for this to work. This has
not been done on your system.

The following step will require write access to
the matplotlib folder. Make sure you have sufficient
rights (become root on a linux system).

Please run the Script configure_matplotlib.py
(in %s)!
This will make two small changes to the installed
matplotlib files and will symlink or copy the file
backend_sv4agg.py to matplotlib.

After a restart of SimuVis4 you should be able to
use matplotlib/pylab in the python console (if the
PythonConsole plugin is active) or in scripts.""")
    ) % os.path.split(__file__)[0]


testCode = """# matplotlib example from the original matplotlib distribution
# Press CTRL-J in the text editor window to run this code!

from pylab import *

matplotlib.use('SV4Agg')

figure(1, figsize=(8,8))
ax = axes([0.1, 0.1, 0.8, 0.8])

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
fracs = [15,30,45, 10]

explode=(0, 0.05, 0, 0)
pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)

show()
"""


def showConfigWarning(*arg):
    QMessageBox.warning(SimuVis4.Globals.mainWin,
        QCoreApplication.translate('MatPlot', 'MatPlot plugin configuration info'),
        configWarningText)


class PlugIn(SimplePlugIn):

    def load(self):
        self.initTranslations()
        cfg = SimuVis4.Globals.config
        cfgsec = self.name.lower()
        if not cfg.has_section(cfgsec):
            cfg.add_section(cfgsec)
        cfg.set_def(cfgsec, 'show_config_warning', 'yes')
        glb = SimuVis4.Globals
        import matplotlib
        self.matplotlib = matplotlib
        try:
            matplotlib.use('SV4Agg')
        except:
            if cfg.getboolean(cfgsec, 'show_config_warning'):
                QTimer().singleShot(2000, self.showConfigWarning)
            raise Exception('matplotlib does not yet support SV4')
        dpath = matplotlib.rcParams['datapath']
        tmp = os.path.join(dpath, 'images')
        if os.path.isdir(tmp):
            dpath = tmp
        winIcon = QIcon(os.path.join(dpath, 'matplotlib.png'))
        testAction = QAction(winIcon,
            QCoreApplication.translate('MatPlot', '&MatPlot Test'), SimuVis4.Globals.mainWin)
        testAction.setStatusTip(QCoreApplication.translate('MatPlot', 'Show a matplotlib test window'))
        QWidget.connect(testAction, SIGNAL("triggered()"), self.test)
        SimuVis4.Globals.mainWin.plugInMenu.addAction(testAction)


    def test(self):
        textEditor = None
        p = SimuVis4.Globals.mainWin.plugInManager
        if p.hasPlugIn('TextEditor'):
            textEditor = SimuVis4.Globals.mainWin.plugInManager.getPlugIn('TextEditor')
        if textEditor:
            w = textEditor.winManager.newWindow()
            w.textEdit.setText(testCode)
        else:
            SimuVis4.Globals.mainWin.executor.run(testCode)
