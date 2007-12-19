# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from PyQt4.QtGui import QWidget, QIcon, QPixmap, QTextBrowser
from PyQt4.QtCore import QCoreApplication, QObject, SIGNAL, QUrl
from SubWin import SubWindow
import Globals, os, webbrowser

externalBrowser = Globals.config.getboolean('main', 'help_browser_external')

helpPath = os.path.join(Globals.config['main:system_help_path'], Globals.config['main:i18n_language'])
if not os.path.isdir(helpPath):
    helpPath = os.path.join(Globals.config['main:system_help_path'], 'en')
helpURL = 'file://' + os.path.join(helpPath, 'index.html')

helpBrowser = None

### FIXME: Add a small webserver here


def showHelp(url=helpURL):
    global helpBrowser
    if externalBrowser:
        webbrowser.open(url, autoraise=1)
    else:
        if not helpBrowser:
            helpBrowser = HelpBrowser(Globals.mainWin.workSpace)
            Globals.mainWin.workSpace.addSubWindow(helpBrowser)
        helpBrowser.browser.setSource(QUrl(url))
        helpBrowser.show()


class HelpBrowser(SubWindow):

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        icon = QIcon(QPixmap(os.path.join(Globals.config['main:system_picture_path'], 'help.xpm')))
        self.setWindowIcon(icon)
        self.setWindowTitle(QCoreApplication.translate('HelpBrowser', 'Help Browser'))
        self.browser = QTextBrowser(self)
        self.setWidget(self.browser)
