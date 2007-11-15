# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from time import time
from SimuVis4.SubWin import SubWindow
from PyQt4.QtGui import QApplication, QDialog, QDialogButtonBox, QVBoxLayout, QGridLayout, QLabel, QLineEdit,\
    QComboBox, QSpinBox, QDoubleSpinBox, QWidget, QCheckBox
from PyQt4.QtCore import QCoreApplication, QTimer, SIGNAL, Qt, QObject

from UI.TimeSignalWidget import Ui_TimeSignalWidget
from UI.ProcessDlg import Ui_ProcessDlg

from Quantities import Text, Choice, Float, Integer, Bool
from Process import Process


class TimeSignalWidget(QWidget, Ui_TimeSignalWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.functions = []
        self.lastValue = 0
        self.startTime = 0
        self.timer = QTimer(self)
        self._foo = False
        self.connect(self.runStopButton, SIGNAL("toggled(bool)"), self.runStop)
        self.connect(self.stepButton, SIGNAL('pressed()'), self.timeOutAction)
        self.connect(self.resetButton, SIGNAL('pressed()'), self.resetTimer)
        self.connect(self.stepSizeInput, SIGNAL('valueChanged(double)'), self.stepSizeChanged)
        self.connect(self.frequencyInput, SIGNAL('valueChanged(double)'), self.frequencyChanged)
        self.connect(self.compValueStepInput, SIGNAL('valueChanged(double)'), self.compValueStepChanged)
        self.connect(self.timer, SIGNAL('timeout()'), self.timeOutAction)

    def stepSizeChanged(self, ss):
        if self._foo: return
        self._foo = True
        self.frequencyInput.setValue(1/ss)
        self.signalRatioLabel.setText('( %g x)' % (self.compValueStepInput.value() / ss))
        self._foo = False        

    def frequencyChanged(self, fr):
        if self._foo: return
        self._foo = True
        self.stepSizeInput.setValue(1/fr)
        self.signalRatioLabel.setText('( %g x)' % (self.compValueStepInput.value()*fr))
        self._foo = False        

    def compValueStepChanged(self, cv):
        if self._foo: return
        self._foo = True
        self.signalRatioLabel.setText('( %g x)' % (cv * self.frequencyInput.value()))
        self._foo = False        

    def resetTimer(self):
        val = self.startValueInput.value()
        self.lastValue = val
        if self.signalShowButton.isChecked():
            self.signalLabel.setText(unicode(val))
        for f in self.functions:
            f(val)

    def runStop(self, t):
        if t:
            self.runStopButton.setText(QCoreApplication.translate('TimeSignalWidget', 'Stop!'))
            if self.realTimeButton.isChecked():
                self.startTime = time()
            self.timeOutAction()
            self.timer.start(self.stepSizeInput.value()*1000)
        else:
            self.runStopButton.setText(QCoreApplication.translate('TimeSignalWidget', 'Run!'))
            self.timer.stop()

    def timeOutAction(self):
        if self.realTimeButton.isChecked():
            val = time() - self.startTime
        else:
            self.lastValue += self.compValueStepInput.value()
            val = self.lastValue
        if self.signalShowButton.isChecked():
            self.signalLabel.setText(unicode(val))
        for f in self.functions:
            f(val)


class TimeSignalWindow(SubWindow):

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('SimTools', 'Time signal Generator'))
        self.timeSignalWidget = TimeSignalWidget(self)
        self.mainLayout.addWidget(self.timeSignalWidget)
        self.setFocusProxy(self.timeSignalWidget)


class SimpleQuantitiesDialog(QDialog):

    def __init__(self, parent=None, windowTitle=''):
        QDialog.__init__(self, parent)
        self.quantities = []
        self.qwidgets   = []
        self.mainLayout = QVBoxLayout(self)
        self.gridLayout = QGridLayout()
        self.mainLayout.addLayout(self.gridLayout)
        self.buttonBox =  QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.NoButton | QDialogButtonBox.Ok)
        self.mainLayout.addWidget(self.buttonBox)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        self.setWindowTitle(windowTitle)

    def addQuantity(self, *l):
        self.addQuantities(l)

    def addQuantities(self, l):
        for q in l:
            i = len(self.quantities)
            self.quantities.append(q)
            l = QLabel(self)
            l.setText(q.descr or q.name)
            self.gridLayout.addWidget(l, i, 0, 1, 1)
            if q.__class__ == Text:
                w = QLineEdit(self)
                if q.maxLen: w.setMaxLength(q.maxLen)
                w.setText(q.v)
            elif q.__class__ == Choice:
                w = QComboBox(self)
                c = [unicode(x) for x in q.choices]
                c.sort()
                w.addItems(c)
                idx = w.findText(unicode(q.v))
                if idx >= 0:
                    w.setCurrentIndex(idx)
            elif q.__class__ == Bool:
                w = QCheckBox(self)
                if q.v:
                    w.setCheckState(Qt.Checked)
                else:
                    w.setCheckState(Qt.Unchecked)
            elif q.__class__ == Integer:
                w = QSpinBox(self)
                w.setMinimum(q.min)
                w.setMaximum(q.max)
                w.setSingleStep(q.step or 0.01)
                if q.unit: w.setSuffix(' '+q.unit)
                w.setValue(q.v)
            elif q.__class__ == Float:
                w = QDoubleSpinBox(self)
                w.setMinimum(q.min)
                w.setMaximum(q.max)
                w.setSingleStep(q.step or 0.01)
                if q.unit: w.setSuffix(' '+q.unit)
                w.setValue(q.v)
            self.gridLayout.addWidget(w, i, 1, 1, 1)
            self.qwidgets.append(w)

    def accept(self):
        for i in range(len(self.quantities)):
            q = self.quantities[i]
            w = self.qwidgets[i]
            if q.__class__ == Text:
                q.set(unicode(w.text()))
            elif q.__class__ == Choice:
                # FIXME: handle non-strings
                q.set(unicode(w.currentText()))
            elif q.__class__ == Bool:
                q.set(w.checkState() == Qt.Checked)
            else:
                q.set(w.value()) # Integer, Float
        QDialog.accept(self)




class ProcessWidget(QWidget, Ui_ProcessDlg):
    """start an external process and show progress"""

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)



class ProcessWindow(SubWindow):

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('SimTools', 'Process'))
        self.processWidget = ProcessWidget(self)
        self.mainLayout.addWidget(self.processWidget)
        self.setFocusProxy(self.processWidget)
