# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from PyQt4.QtGui import QWidget, QIcon, QPixmap
from PyQt4.QtCore import QCoreApplication, QObject, SIGNAL, QUrl
from SubWin import SubWindow
from UI.HelpBrowser import Ui_HelpBrowserWidget
import Globals, os

helpFilePath = os.path.join(Globals.config['main:system_help_path'], Globals.config['main:i18n_language'])
if not os.path.isdir(helpFilePath):
    helpFilePath = os.path.join(Globals.config['main:system_help_path'], 'en')

# FIXME: this is far from being complete ...

class HelpBrowserWidget(QWidget, Ui_HelpBrowserWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.textBrowser.setSearchPaths([helpFilePath])
        self.textBrowser.setSource(QUrl('index.html'))


class HelpBrowser(SubWindow):

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        icon = QIcon(QPixmap(os.path.join(Globals.config['main:system_picture_path'], 'help.xpm')))
        self.setWindowIcon(icon)
        self.setWindowTitle(QCoreApplication.translate('HelpBrowser', 'Help Browser'))
        self.browser = HelpBrowserWidget(self)
        self.mainLayout.addWidget(self.browser)
        self.setFocusProxy(self.browser)
        QObject.connect(self.browser.closeButton, SIGNAL("pressed()"), self.close)

    def showHelp(self, context=None, topic=None):
        self.show()
        #FIXME: show topic

    def addSource(self, context, document):
        pass
