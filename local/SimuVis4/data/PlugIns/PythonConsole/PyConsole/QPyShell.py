# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import os, sys, string

from PyQt4.QtGui import QWidget, QTextCursor, QPrintDialog, QPrinter,\
    QDialog, QFileDialog, QMessageBox, QInputDialog, QTextEdit, QGroupBox,\
    QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QToolButton, QSpacerItem, \
    QSizePolicy, QPushButton
from PyQt4.QtCore import SIGNAL, Qt, QSize, QCoreApplication
from code import InteractiveInterpreter
from Completer import Completer


identChars = string.letters + string.digits + '_.'

def mydisplayhook(a):
    """Simple function to "write" an object to stdout. This is needed because
    sys.displayhook stores the last output in __builtin__._, which conflicts
    with the gettext module."""
    if a is not None:
        sys.stdout.write("%r" % (a,))


class DummyFileW(object):
    """File-like object that will delegate write()-calls to another function"""
    def __init__(self, wfunc):
        self.wfunc = wfunc

    def write(self, s):
        self.wfunc(s)

    def flush(self):
        pass


greeting = QCoreApplication.translate("QPyShell", """<h3> +++ Welcome to the python shell +++ </h3>
<i>You may enter arbitrary python code at the prompt above, 
line by line. Please use spaces instead of tabs for indentation! 
[Enter] will accept a line. Press [UP] and [DOWN] or [ESC] for command line history.
[Shift+Enter] invokes autocompletion of identifiers.
</i>""")

def formatPyLine(l):
    """format a python command line for the output buffer"""
    # FIXME: escape characters with special meaning in HTML
    tmp = l.lstrip(' ')
    return '&bull;' * (len(l)-len(tmp)) + tmp


class QPyShell(QWidget):
    """QPyShell - a Qt based python command shell based on code.InteractiveInterpreter.
    Because it catches stdout and stderr there can be only one active instance of this
    class. Make sure initInterpreter() and exitInterpreter() is called!
    """

    activeInstance = None

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        if parent:
            self.standalone = False
        else:
            self.standalone = True

        self.setWindowTitle(QCoreApplication.translate("QPyShell", "QPyShell - a simple python shell widget for Qt"))

        self.clBox = QGroupBox(self)
        self.clBox.setTitle(QCoreApplication.translate("QPyShell", "Python command input"))

        self.promptLabel = QLabel(self.clBox)
        self.promptLabel.setText(">>>")
        self.lineInput = QLineEdit(self.clBox)
        self.enterButton = QToolButton(self.clBox)
        self.enterButton.setArrowType(Qt.RightArrow)

        self.clLayout = QHBoxLayout(self.clBox)
        self.clLayout.addWidget(self.promptLabel)
        self.clLayout.addWidget(self.lineInput)
        self.clLayout.addWidget(self.enterButton)

        self.outputBrowser = QTextEdit(self)
        self.outputBrowser.setMinimumSize(QSize(100,100))
        self.outputBrowser.setReadOnly(True)

        self.saveButton = QPushButton(self)
        self.saveButton.setText(QCoreApplication.translate("QPyShell", "Save ..."))
        self.clearButton = QPushButton(self)
        self.clearButton.setText(QCoreApplication.translate("QPyShell", "Clear"))

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addItem(QSpacerItem(27, 29, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.buttonLayout.addWidget(self.saveButton)
        self.buttonLayout.addWidget(self.clearButton)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.outputBrowser)
        self.mainLayout.addWidget(self.clBox)
        self.mainLayout.addLayout(self.buttonLayout)

        self.history = []
        self.historyFile = None
        self.history_i = -1
        self.cmdBuffer = []
        self.showCompletionLimit = 100
        self.interpreter = None
        self.old_displayhook = None
        self.cursor = QTextCursor(self.outputBrowser.document())
        self.outputBrowser.setTextCursor(self.cursor)
        self.outputBrowser.append(greeting)

        self.setTabOrder(self.lineInput, self.outputBrowser)
        self.setTabOrder(self.outputBrowser, self.enterButton)
        self.setTabOrder(self.enterButton, self.saveButton)
        self.setTabOrder(self.saveButton, self.clearButton)

        self.connect(self.enterButton, SIGNAL("pressed()"), self.run)
        self.connect(self.saveButton, SIGNAL("pressed()"), self.saveContents)
        self.connect(self.clearButton, SIGNAL("pressed()"), self.outputBrowser.clear)


    def initInterpreter(self, loc=None, greet=greeting, historyFile=None):
        if QPyShell.activeInstance:
            raise Exception(QCoreApplication.translate("QPyShell", "QPyShell: There can be only one highlander... sorry, I mean one active QPyShell widget!"))
        QPyShell.activeInstance = self
        self.loadHistoryFile(historyFile)
        self.interpreter = InteractiveInterpreter(loc)
        self.completer = Completer(loc)
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = DummyFileW(self.write)
        sys.stderr = sys.stdout
        # there's a strange problem with gettext and interactive interpreters
        # gettext's "_"" will be overwritten by the standard sys.displayhook...
        self.old_displayhook = sys.displayhook
        sys.displayhook = mydisplayhook


    def loadHistoryFile(self, historyFile):
        self.historyFile = historyFile
        if historyFile and os.path.exists(historyFile):
            lines = open(historyFile, 'r').read().split(os.linesep)
            self.history = [l for l in lines if not l.startswith('#')]


    def saveHistoryFile(self):
        if self.historyFile:
            h = self.history
            if len(h) > 100:
                h = h[:100]
            h.insert(0, unicode(QCoreApplication.translate('QPyShell', '# this is the command history of the QPyShell')))
            open(self.historyFile, 'w').write(os.linesep.join(h))


    def exitInterpreter(self, loc=None):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.saveHistoryFile()
        del self.interpreter
        self.interpreter = None
        sys.displayhook = self.old_displayhook
        QPyShell.ativeInstance = None


    def run(self):
        if not self.interpreter:
            raise Exception(QCoreApplication.translate("QPyShell", "No interpreter found! You need to call QPyShell.initInterpreter() first!"))
        line = unicode(self.lineInput.text())
        self.lineInput.clear()
        if line:
            if (not self.history) or line != self.history[0]:
                # no consecutive identical entries
                self.history.insert(0, line)
            self.history_i = -1
            self.cursor.movePosition(QTextCursor.End)
            if not self.cmdBuffer:
                self.outputBrowser.append('<hr>|<b>&nbsp;%s</b><br>' % formatPyLine(line))
            else:
                self.outputBrowser.append('|<b>&nbsp;%s</b><br>' % formatPyLine(line))
            self.cursor.movePosition(QTextCursor.End)
            self.outputBrowser.ensureCursorVisible()
        self.cmdBuffer.append(line)
        more = self.interpreter.runsource('\n'.join(self.cmdBuffer))
        if more:
            self.promptLabel.setText('...')
        else:
            self.cmdBuffer = []
            self.promptLabel.setText('>>>')


    def write(self, s):
        self.cursor.movePosition(QTextCursor.End)
        self.outputBrowser.insertPlainText(s)
        self.cursor.movePosition(QTextCursor.End)
        self.outputBrowser.ensureCursorVisible()


    def keyPressEvent(self, event):
        key = event.key()
        mod = event.modifiers()
        if key == Qt.Key_Up and self.history:
            self.history_i = min(self.history_i+1, len(self.history)-1)
            self.lineInput.setText(self.history[self.history_i])
        elif key == Qt.Key_Down and self.history:
            self.history_i = max(self.history_i-1, -1)
            if self.history_i >= 0:
                self.lineInput.setText(self.history[self.history_i])
            else:
                self.lineInput.setText('')
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            if mod & Qt.ShiftModifier:
                self.complete()
            else:
                self.run()
        elif key == Qt.Key_Escape:
            txt, r = QInputDialog.getItem(self, QCoreApplication.translate("QPyShell", "Command line history"),
                QCoreApplication.translate("QPyShell", "Please select a history item:"),
                self.history, 0, False)
            if r and txt:
                self.lineInput.setText(txt)
        elif self.standalone and key == Qt.Key_Print:
            self.printContents()
        elif self.standalone and key == Qt.Key_Q and (mod & Qt.ControlModifier):
            self.close()
        else:
            QWidget.keyPressEvent(self, event)


    def closeEvent(self, event):
        if self.standalone:
            self.exitInterpreter()
        QWidget.closeEvent(self, event)


    def printContents(self, printer=None):
        if not printer:
            printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle(QCoreApplication.translate("QPyShell", "Print Document"))
        if dialog.exec_() != QDialog.Accepted:
            return
        self.outputBrowser.document().print_(printer)


    def saveContents(self, fileName=None):
        if not fileName:
            fileTypes = {'Text':('txt',), 'HTML':('htm', 'html')}
            filters = ';;'.join(['%s (%s)' % (k, ' '.join(['*.'+e for e in v])) for k, v in fileTypes.items()])
            dlg = QFileDialog(self,
                QCoreApplication.translate('QPyShell', 'Select name of file to save'),
                os.getcwd(), filters)
            dlg.setFileMode(QFileDialog.AnyFile)
            dlg.setAcceptMode(QFileDialog.AcceptSave)
            if dlg.exec_() != QDialog.Accepted:
                return
            tmp = unicode(dlg.selectedFilter())
            fileType = tmp[:tmp.find('(')-1]
            dlg.setDefaultSuffix(fileTypes[fileType][0])
            files = dlg.selectedFiles()
            if not files:
                return
            fileName = unicode(files[0])
        if fileType == 'Text':
            txt = self.outputBrowser.toPlainText()
        elif fileType == 'HTML':
            txt = self.outputBrowser.toHtml()
        else:
            raise IOError('Unknown FileType: %s' % fileType)
        try:
            open(fileName, 'w').write(txt)
        except IOError:
            QMessageBox.critical(self,
                QCoreApplication.translate('QPyShell', 'Could not save file!'),
                QCoreApplication.translate('QPyShell', 'Writing failed! Make sure you have write permissions!'))


    def complete(self):
        """ a very simple, quick and dirty completion of identifiers in the namespace """
        # FIXME: fertig machen!
        txt = unicode(self.lineInput.text())
        cur = self.lineInput.cursorPosition()
        s = cur
        while s>0 and txt[s-1] in identChars:
            s -= 1
        try:
            completions = self.completer.matches(txt[s:cur])
        except:
            return
        if not completions:
            return
        n_comp = len(completions)
        if n_comp == 1:
            comp = completions.pop()
            self.lineInput.insert(comp[cur-s:])
        elif n_comp < self.showCompletionLimit:
            tmp = list(completions)
            tmp.sort()
            txt = '<font color="#0000ff">[%s]</font>' % ', '.join(tmp)
            self.outputBrowser.append(txt)
            # get common prefix ... stolen from the python cookbook
            pref = tmp[0][:([min([x[0]==elem for elem in x]) for x in zip(*tmp)]+[0]).index(0)]
            if len(pref) > (cur-s):
                self.lineInput.insert(pref[cur-s:])
        else:
            self.outputBrowser.append(unicode(QCoreApplication.translate("QPyShell",
                '<font color="#0000ff">[Too many completions: %d]</font>')) % n_comp)


if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    if sys.platform == 'linux2':
        historyFile = os.path.join(os.environ['HOME'], '.QPyShell.hist')
    elif platform == 'win32':
        historyFile = os.path.join(os.environ['USERPROFILE'], 'QPyShell.hist')
    else:
        historyFile = None
    app = QApplication(sys.argv)
    w = QPyShell()
    w.setMinimumSize(800, 600)
    w.show()
    w.initInterpreter(loc=globals(), historyFile=historyFile)
    sys.exit(app.exec_())
