# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from PyQt4.QtGui import QWidget, QPixmap, QIcon, QDialog, QPrintDialog, QMessageBox, QFileDialog, QPrinter
from PyQt4.QtCore import SIGNAL, QCoreApplication
from SubWin import SubWindow
from UI.LogView import Ui_LogViewWidget
from logging import *
import Globals, Errors, os

# FIXME: levels dynamisch bestimmen?
levels = (DEBUG, INFO, WARNING, ERROR, CRITICAL)
levelInfo = [(getLevelName(l), l) for l in levels]

# FIXME: hier noch einen schoenen HTML-Formatter basteln
# messages in list-buffer halten ?

class TextBrowserHandler(Handler):

    def setBrowser(self, b):
        self.browser = b

    def emit(self, r):
        self.browser.append(self.format(r))


class LogViewWidget(QWidget, Ui_LogViewWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)


class LogWindow(SubWindow):

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        icon = QIcon(QPixmap(os.path.join(Globals.config['main:system_picture_path'], 'logwin.xpm')))
        self.setWindowIcon(icon)
        self.setWindowTitle(QCoreApplication.translate('LogWindow', 'Log Messages'))
        self.setMinimumSize(500, 100)
        self.logView = LogViewWidget(self)
        self.mainLayout.addWidget(self.logView)
        self.setFocusProxy(self.logView)
        self.logView.ThresholdSelector.addItems([l[0] for l in levelInfo])
        self.handler = TextBrowserHandler()
        self.handler.setBrowser(self.logView.TextArea)
        self.logView.ThresholdSelector.setCurrentIndex(0)
        self.setThreshold(0)
        self.connect(self.logView.SaveButton, SIGNAL("pressed()"), self.saveWindow)
        self.connect(self.logView.ThresholdSelector, SIGNAL("activated(int)"), self.setThreshold)
        self.hideOnClose = True
        self.toggleVisibleAction.setIcon(icon)
        self.toggleVisibleAction.setText(QCoreApplication.translate('LogWindow', '&Log window'))
        self.toggleVisibleAction.setShortcut(QCoreApplication.translate('LogWindow', 'Ctrl+L'))
        self.toggleVisibleAction.setStatusTip(QCoreApplication.translate('LogWindow', 'Log window'))


    def setThreshold(self, t):
        self.handler.setLevel(levelInfo[t][1])


    def printWindow(self, printer=None):
        if not printer:
            printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle(QCoreApplication.translate('LogWindow', 'Print Document'))
        if dialog.exec_() != QDialog.Accepted:
            return
        self.logView.TextArea.document().print_(printer)


    def saveWindow(self, fileName=None, fileType=None):
        if not fileName:
            fileTypes = {'Text':('txt',), 'HTML':('htm', 'html')}
            filters = ';;'.join(['%s (%s)' % (k, ' '.join(['*.'+e for e in v])) for k, v in fileTypes.items()])
            dlg = QFileDialog(self,
                QCoreApplication.translate('LogWindow', 'Select name of file to save'),
                Globals.defaultFolder or '', filters)
            dlg.setFileMode(QFileDialog.AnyFile)
            dlg.setAcceptMode(QFileDialog.AcceptSave)
            if dlg.exec_() != QDialog.Accepted:
                return
            tmp = str(dlg.selectedFilter())
            fileType = tmp[:tmp.find('(')-1]
            dlg.setDefaultSuffix(fileTypes[fileType][0])
            files = dlg.selectedFiles()
            if not files:
                return
            fileName = unicode(files[0])
            Globals.defaultFolder, tmp = os.path.split(fileName)
        if fileType == 'Text':
            txt = self.logView.TextArea.toPlainText()
        elif fileType == 'HTML':
            txt = self.logView.TextArea.toHtml()
        else:
            raise Errors.IOError('Unknown FileType: %s' % fileType)
        try:
            open(fileName, 'w').write(txt)
        except IOError:
            QMessageBox.critical(self,
                QCoreApplication.translate('LogWindow', 'Could not save file!'),
                QCoreApplication.translate('LogWindow', 'Writing failed! Make sure you have write permissions!'))
