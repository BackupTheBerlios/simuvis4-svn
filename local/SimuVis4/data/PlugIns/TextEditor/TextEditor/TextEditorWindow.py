# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from SimuVis4.SubWin import SubWindow
from SimuVis4.Errors import IOError
import SimuVis4.Globals, os
from PyQt4.QtGui import QTextEdit, QFileDialog, QPrintDialog, QPrinter, QDialog
from PyQt4.QtCore import SIGNAL, QCoreApplication


# FIXME: add a changed-flag!

class TextEditorWindow(SubWindow):
    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('TextEditor', 'Text editor'))
        self.textEdit = QTextEdit(self)
        self.mainLayout.addWidget(self.textEdit)
        self.setFocusProxy(self.textEdit)
        self.resize(600, 300)
        self.fileName = None


    def setFileName(self, fileName):
        self.fileName = fileName
        self.setWindowTitle(fileName)


    def load(self, fileName=None):
        if not fileName:
            fileName = 'Unnamed'
        self.setFileName(fileName)
        try:
            txt = open(fileName, 'r').read()
            self.textEdit.setPlainText(txt)
        except:
            raise IOError(unicode(QCoreApplication.translate('TextEditor', 'TextEditor: could not read file: %s')) % fileName)


    def save(self):
        if not self.fileName:
            self.setFileName(self.askForFileName())
        if not self.fileName:
            return False
        try:
            txt = self.textEdit.toPlainText()
            open(self.fileName, 'w').write(unicode(txt))
            return True
        except:
            raise IOError(unicode(QCoreApplication.translate('TextEditor', 'TextEditor: could not write file: %s')) % self.fileName)


    def saveAs(self, fileName=None):
        if not fileName:
            fileName = self.askForFileName()
        if not fileName:
            return False
        self.setFileName(fileName)
        self.save(w)
        return True


    def askForFileName(self):
        fileName = unicode(QFileDialog.getSaveFileName(self, QCoreApplication.translate('TextEditor',
            "Select file to save"), SimuVis4.Globals.defaultFolder))
        if fileName:
            SimuVis4.Globals.defaultFolder, tmp = os.path.split(fileName)
        return fileName


    def closeEvent(self, e):
        # FIXME: try to save file if changed!
        SubWindow.closeEvent(self, e)
        #e.accept()


    def printWindow(self, printer=None):
        if not printer:
            printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle(QCoreApplication.translate('TextEditor', 'Print Document'))
        if dialog.exec_() != QDialog.Accepted:
            return
        self.textEdit.document().print_(printer)
