# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""TextEditor PlugIn for SimuVis4 - provides simple text editing"""

import SimuVis4, os
from SimuVis4.SubWinManager import SubWinManager
from SimuVis4.PlugIn import SimplePlugIn
import TextEditorWindow
from PyQt4.QtGui import QAction, QIcon, QWidget, QPixmap, QMenu, QFileDialog
from PyQt4.QtCore import SIGNAL, QCoreApplication, QObject


class PlugIn(SimplePlugIn):

    def load(self):
        xpm = QPixmap()
        xpm.loadFromData(self.getFile('text.xpm').read())
        winIcon = QIcon(xpm)
        self.winManager = TextEditorManager(SimuVis4.Globals.mainWin.workSpace, TextEditorWindow.TextEditorWindow,
            QCoreApplication.translate('TextEditor', "Unnamed Textfile"), winIcon)
        self.winManager.initMain(SimuVis4.Globals.mainWin)


    def unload(self, fast):
        if self.winManager:
            self.winManager.shutdown()
            del self.winManager


    def test(self):
        if self.winManager:
            self.winManager.newWindow()


    def listWindows(self):
        if self.winManager:
            return winManager.windows



class TextEditorManager(SubWinManager):

    def initMain(self, mainWin):
        self.mainWin = mainWin
        menu = QMenu(QCoreApplication.translate('TextEditor', 'Text files'))

        self.fileNewAction = QAction(QIcon(), QCoreApplication.translate('TextEditor', '&New'),
            self.mainWin)
        self.fileNewAction.setShortcut(QCoreApplication.translate('TextEditor', "Ctrl+N"))
        self.fileNewAction.setStatusTip(QCoreApplication.translate('TextEditor', 'New file'))
        QObject.connect(self.fileNewAction, SIGNAL("triggered()"), self.newWindow)
        menu.addAction(self.fileNewAction)

        self.fileOpenAction = QAction(QIcon(), QCoreApplication.translate('TextEditor', '&Open'),
            self.mainWin)
        self.fileOpenAction.setShortcut(QCoreApplication.translate('TextEditor', "Ctrl+O"))
        self.fileOpenAction.setStatusTip(QCoreApplication.translate('TextEditor', 'Open file'))
        QObject.connect(self.fileOpenAction, SIGNAL("triggered()"), self.openFile)
        menu.addAction(self.fileOpenAction)

        self.fileSaveAction = QAction(QIcon(), QCoreApplication.translate('TextEditor', '&Save'),
            self.mainWin)
        self.fileSaveAction.setShortcut(QCoreApplication.translate('TextEditor', "Ctrl+S"))
        self.fileSaveAction.setStatusTip(QCoreApplication.translate('TextEditor', 'Save file'))
        QObject.connect(self.fileSaveAction, SIGNAL("triggered()"), self.save)
        menu.addAction(self.fileSaveAction)

        self.fileSaveAsAction = QAction(QIcon(), QCoreApplication.translate('TextEditor', '&Save as ...'),
            self.mainWin)
        self.fileSaveAsAction.setStatusTip(QCoreApplication.translate('TextEditor', 'Save file as ...'))
        QObject.connect(self.fileSaveAsAction, SIGNAL("triggered()"), self.save)
        menu.addAction(self.fileSaveAsAction)

        self.fileCloseAction = QAction(QIcon(), QCoreApplication.translate('TextEditor', '&Close'),
            self.mainWin)
        self.fileCloseAction.setShortcut(QCoreApplication.translate('TextEditor', "Ctrl+W"))
        self.fileCloseAction.setStatusTip(QCoreApplication.translate('TextEditor', 'Save file'))
        QObject.connect(self.fileCloseAction, SIGNAL("triggered()"), self.closeWindow)
        menu.addAction(self.fileCloseAction)

        self.fileRunAction = QAction(QIcon(), QCoreApplication.translate('TextEditor', '&Run'),
            self.mainWin)
        self.fileRunAction.setShortcut(QCoreApplication.translate('TextEditor', "Ctrl+J"))
        self.fileRunAction.setStatusTip(QCoreApplication.translate('TextEditor', 'Run current file'))
        QObject.connect(self.fileRunAction, SIGNAL("triggered()"), self.runScript)
        menu.addAction(self.fileRunAction)

        self.menu = menu
        self.separator = self.mainWin.fileMenu.insertSeparator(self.mainWin.fileMenuSeparator)
        self.mainWin.fileMenu.insertMenu(self.mainWin.fileMenuSeparator, menu)

    def openFile(self, w=None):
        fn = unicode(QFileDialog.getOpenFileName(self.workSpace,
            QCoreApplication.translate('TextEditor', "Select file to open"), SimuVis4.Globals.defaultFolder))
        if fn:
            SimuVis4.Globals.defaultFolder, tmp = os.path.split(fn)
            w = self.newWindow()
            w.load(fn)

    def save(self, w=None):
        if not w:
            w = self.getActiveWindow()
        if w:
            w.save()

    def saveAs(self, w=None):
        if not w:
            w = self.getActiveWindow()
        if w:
            w.saveAs()

    def runScript(self, w=None):
        if not w:
            w = self.getActiveWindow()
        if w:
            txt = unicode(w.textEdit.toPlainText())
            if txt:
                self.mainWin.executor.run(txt, name=w.fileName)

    def shutdown(self):
        del self.menu
        del self.separator


