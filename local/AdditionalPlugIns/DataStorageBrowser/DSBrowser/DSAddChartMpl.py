# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, Icons
from PyQt4.QtGui import QWidget, QIcon, QPixmap, QWizard
from PyQt4.QtCore import QTimer, SIGNAL, QDateTime



class AddChartWizard(QWizard):

    def __init__(self, parent):
        QWizard.__init__(self, parent)



def showAddChartWizard(sensorgroup):
    wiz = AddChartWizard(None)
    wiz.exec_()
