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

mplMinVersion = '0.90'
mplMaxVersion = '0.91.1'

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
PythonConsole plugin is active) or in scripts."""
)) % os.path.split(__file__)[0]


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
        cfg.set_def(cfgsec, 'set_default_backend', 'yes')
        cfg.set_def(cfgsec, 'show_config_warning', 'yes')
        cfg.set_def(cfgsec, 'zoom_step_factor', '0.189207115002721')
        cfg.set_def(cfgsec, 'mouse_wheel_step', '15')
        glb = SimuVis4.Globals
        import matplotlib
        if matplotlib.__version__ < mplMinVersion or matplotlib.__version__ > mplMaxVersion:
            SimuVis4.Globals.logger.error(unicode(QCoreApplication.translate('MatPlot', 'MatPlot: need matplotlib version between %s and %s, but found %s')) % \
                (mplMinVersion, mplMaxVersion, matplotlib.__version__))
            return False
        self.matplotlib = matplotlib
        if cfg.getboolean(cfgsec, 'set_default_backend'):
            try:
               matplotlib.use('SV4Agg')
            except:
               if cfg.getboolean(cfgsec, 'show_config_warning'):
                   QTimer().singleShot(8000, showConfigWarning)
        import backend_sv4agg
        self.backend_sv4agg = backend_sv4agg
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
        return True


    def test(self):
        testCode = self.getFile('mpl_test_contour.py').read()
        try:
            w = SimuVis4.Globals.plugInManager['TextEditor'].winManager.newWindow('MatPlot test')
            w.textEdit.setText(testCode)
        except:
            SimuVis4.Globals.executor.run(testCode)
