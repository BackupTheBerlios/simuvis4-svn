# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from PyQt4.QtGui import QWidget, QPixmap, QIcon, QDialog, QPrintDialog, QMessageBox, QFileDialog, QPrinter
from PyQt4.QtCore import SIGNAL, QCoreApplication
from SubWin import SubWindow
from UI.LogView import Ui_LogViewWidget
from logging import *
import Globals, Errors, Icons, os


class TextBrowserHandler(Handler):

    def setBrowser(self, b, w):
        self.browser = b
        self.win = w
        self.raiseLevel = Globals.logLevels.get(Globals.config['main:log_raise_level'], CRITICAL)
        self.setFormatter(Formatter('<b>%(levelname)s</b> (<i>%(module)s</i>): %(message)s'))

    def emit(self, r):
        self.browser.append(self.format(r))
        if r.levelno >= self.raiseLevel:
            if not self.win.isVisible():
                self.win.toggleVisibleAction.setChecked(True)
            if self.win.isMinimized():
                self.win.showNormal()
            self.win.raise_()


class LogViewWidget(QWidget, Ui_LogViewWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.SaveButton.setIcon(QIcon(QPixmap(Icons.fileSave)))
        self.ClearButton.setIcon(QIcon(QPixmap(Icons.clear)))


class LogWindow(SubWindow):

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        icon = QIcon(QPixmap(os.path.join(Globals.config['main:system_picture_path'], 'logwin.xpm')))
        self.setWindowIcon(icon)
        self.setWindowTitle(QCoreApplication.translate('LogWindow', 'Log Messages'))
        self.setMinimumSize(500, 100)
        self.logView = LogViewWidget(self)
        self.setWidget(self.logView)
        tmp = Globals.logLevels.items()
        tmp.sort(lambda a,b: cmp(a[1], b[1]))
        self.levels = [l[0] for l in tmp]
        self.logView.ThresholdSelector.addItems(self.levels)
        self.handler = TextBrowserHandler()
        self.handler.setBrowser(self.logView.TextArea, self)
        try:
            i = self.levels.index(Globals.config['main:log_threshold'])
            self.logView.ThresholdSelector.setCurrentIndex(i)
            self.setThreshold(i)
        except:
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
        l = Globals.logLevels[self.levels[t]]
        Globals.logger.setLevel(l)

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
