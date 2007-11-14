# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from SubWin import SubWindow
from UI.TaskBrowser import Ui_TaskBrowserWidget
import Globals, os


class TaskBrowserWidget(QWidget, Ui_TaskBrowserWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        
class TaskBrowser(SubWindow):
    
    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        icon = QIcon(QPixmap(os.path.join(Globals.config['main:system_picture_path'], 'taskwin.xpm')))
        self.setWindowIcon(icon)
        self.setWindowTitle(QCoreApplication.translate('TaskBrowser', 'Tasks'))
        self.browser = TaskBrowserWidget(self)
        self.mainLayout.addWidget(self.browser)
        self.setFocusProxy(self.browser)
        
        self.toggleVisibleAction.setIcon(icon)
        self.toggleVisibleAction.setText(QCoreApplication.translate('TaskBrowser', '&Task browser'))
        self.toggleVisibleAction.setShortcut(QCoreApplication.translate('TaskBrowser', "Ctrl+T"))
        self.toggleVisibleAction.setStatusTip(QCoreApplication.translate('TaskBrowser', 'Task Browser'))
