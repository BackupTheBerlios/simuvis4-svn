# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from time import time
from SimuVis4.SubWin import SubWindow
from PyQt4.QtGui import QWidget 
from PyQt4.QtCore import QCoreApplication, QTimer, SIGNAL
from UI.TimeSignalWidget import Ui_TimeSignalWidget
from UI.ProcessDlg import Ui_ProcessDlg



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
        self.setWidget(self.timeSignalWidget)


# FIXME: ProcessWidget does not work yet

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
        self.setWidget(self.processWidget)

