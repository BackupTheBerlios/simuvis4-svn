# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from time import time
from SimuVis4.SubWin import SubWindow
from PyQt4.QtGui import QApplication, QDialog, QDialogButtonBox, QVBoxLayout, QGridLayout, QLabel, QLineEdit,\
    QComboBox, QSpinBox, QDoubleSpinBox, QWidget, QCheckBox, QScrollArea, QFrame, QTextEdit,\
    QListWidget, QAbstractItemView, QDateTimeEdit, QHBoxLayout, QSizePolicy, QToolButton
from PyQt4.QtCore import QCoreApplication, QTimer, SIGNAL, Qt, QObject, QDateTime, QSize, QRect

from UI.TimeSignalWidget import Ui_TimeSignalWidget
from UI.ProcessDlg import Ui_ProcessDlg

from Quantities import Text, MLText, Choice, MultiChoice, Float, Integer, Bool, DateTime
from Process import Process


quantityClasses = {
    unicode(QCoreApplication.translate('QuantitiesDialog', 'Simple Text')): Text,
    unicode(QCoreApplication.translate('QuantitiesDialog', 'Multiline Text')): MLText,
    unicode(QCoreApplication.translate('QuantitiesDialog', 'Single Choice')): Choice,
    unicode(QCoreApplication.translate('QuantitiesDialog', 'Multiple Choice')): MultiChoice,
    unicode(QCoreApplication.translate('QuantitiesDialog', 'Boolean')): Bool,
    unicode(QCoreApplication.translate('QuantitiesDialog', 'Integer')): Integer,
    unicode(QCoreApplication.translate('QuantitiesDialog', 'Float')): Float,
    unicode(QCoreApplication.translate('QuantitiesDialog', 'Date+Time')): DateTime
}


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



class QuantityWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout = QGridLayout(self)
        self.quantities = []
        self.qwidgets   = []
        self.qlabels = []

    def addQuantities(self, l):
        """set the list of quantities"""
        for q in l:
            i = len(self.quantities)
            self.quantities.append(q)
            l = QLabel(self)
            self.qlabels.append(l)
            l.setText(q.name)
            l.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
            l.setToolTip(q.descr)
            self.gridLayout.addWidget(l, i, 0, 1, 1)
            cls = q.__class__
            if cls == Text:
                w = QLineEdit(self)
                w.setMinimumSize(300, 30)
                if q.maxLen: w.setMaxLength(q.maxLen)
                print q.v
                w.setText(q.v)
            elif cls == MLText:
                w = QTextEdit(self)
                w.setAcceptRichText(False)
                w.setMinimumSize(300, 60)
                w.setText(q.v)
            elif cls == Choice:
                w = QComboBox(self)
                c = [unicode(x) for x in q.choices]
                c.sort()
                w.addItems(c)
                idx = w.findText(unicode(q.v))
                if idx >= 0:
                    w.setCurrentIndex(idx)
            elif cls == MultiChoice:
                w = QListWidget(self)
                w.setSelectionMode(QAbstractItemView.MultiSelection)
                w.setMinimumSize(100, 60)
                c = [unicode(x) for x in q.choices]
                c.sort()
                v = [unicode(x) for x in q.v]
                for ii, s in enumerate(c):
                    w.addItem(s)
                    if s in v:
                        w.item(ii).setSelected(True)
            elif cls == Bool:
                w = QCheckBox(self)
                if q.v:
                    w.setCheckState(Qt.Checked)
                else:
                    w.setCheckState(Qt.Unchecked)
            elif cls == Integer:
                w = QSpinBox(self)
                if q.min is not None:
                    w.setMinimum(q.min)
                if q.max is not None:
                    w.setMaximum(q.max)
                if q.step is not None:
                    w.setSingleStep(q.step or 0.01)
                if q.unit: w.setSuffix(' '+q.unit)
                w.setValue(q.v)
            elif cls == Float:
                w = QDoubleSpinBox(self)
                if q.min is not None:
                    w.setMinimum(q.min)
                if q.max is not None:
                    w.setMaximum(q.max)
                w.setSingleStep(q.step or 0.01)
                if q.unit: w.setSuffix(' '+q.unit)
                w.setValue(q.v)
            elif cls == DateTime:
                w = QDateTimeEdit(self)
                w.setCalendarPopup(True)
                dt = QDateTime()
                dt.setTime_t(q.v)
                w.setDateTime(dt)
                if q.min is not None:
                    mindt = QDateTime()
                    mindt.setTime_t(q.min)
                    w.setMinimumDate(mindt.date())
                if q.max is not None:
                    maxdt = QDateTime()
                    maxdt.setTime_t(q.max)
                    w.setMaximumDate(mindt.date())
            l.setBuddy(w)
            w.setToolTip(q.descr)
            w.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            w.adjustSize()
            self.gridLayout.addWidget(w, i, 1, 1, 1)
            self.qwidgets.append(w)
        self.adjustSize()


    def delQuantities(self, *names):
        """delete Quantities by name, widgets get disabled but not deleted"""
        qq = [q for q in self.quantities if q and q.name in names]
        for q in qq:
            i = self.quantities.index(q)
            self.quantities[i] = None
            self.qwidgets[i].setEnabled(False)
            self.qlabels[i].setEnabled(False)


    def applyChanges(self):
        for i in range(len(self.quantities)):
            q = self.quantities[i]
            if q is not None:
                w = self.qwidgets[i]
                cls = q.__class__
                if cls == Text:
                    q.set(unicode(w.text()))
                elif cls == MLText:
                    q.set(unicode(w.toPlainText()))
                elif cls == Choice:
                    q.set(unicode(w.currentText()))
                elif cls == MultiChoice:
                    q.set([unicode(ii.text()) for ii in w.selectedItems()])
                elif cls == Bool:
                    q.set(w.checkState() == Qt.Checked)
                elif cls == DateTime:
                    q.set(w.dateTime().toTime_t())
                else:
                    q.set(w.value()) # Integer, Float
        return [q for q in self.quantities if q is not None]



class SimpleQuantitiesDialog(QDialog):
    """Simple dialog to display and change quantities"""

    def __init__(self, parent=None, windowTitle='', scrolling=True, text=''):
        QDialog.__init__(self, parent)
        self.mainLayout = QVBoxLayout(self)
        self.textLabel = QLabel(self)
        self.textLabel.setText(text)
        self.mainLayout.addWidget(self.textLabel)
        if scrolling:
            self.scrollArea = QScrollArea(self)
            self.mainLayout.addWidget(self.scrollArea)
            self.quantityWidget = QuantityWidget(self.scrollArea)
            self.scrollArea.setWidget(self.quantityWidget)
            self.scrollArea.setWidgetResizable(False)
        else:
            self.quantityWidget = QuantityWidget(self)
            self.mainLayout.addWidget(self.quantityWidget)
        self.buttonBox =  QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.NoButton | QDialogButtonBox.Ok)
        self.mainLayout.addWidget(self.buttonBox)
        QObject.connect(self.buttonBox, SIGNAL('accepted()'), self.accept)
        QObject.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)
        self.setWindowTitle(windowTitle)
        self.result = None

    def addQuantities(self, l):
        """set the list of quantities"""
        self.quantityWidget.addQuantities(l)

    def accept(self):
        """after dialog closes, quantity list is available as self.result"""
        self.result = self.quantityWidget.applyChanges()
        QDialog.accept(self)



class ComplexQuantitiesDialog(SimpleQuantitiesDialog):
    """complex dialog to display, change, add or delete quantities"""

    def __init__(self, parent=None, windowTitle='', scrolling=True, text=''):
        SimpleQuantitiesDialog.__init__(self, parent, windowTitle, scrolling, text)
        self.editButtonLayout = QHBoxLayout()
        self.mainLayout.insertLayout(2, self.editButtonLayout)
        self.addButton = QToolButton(self)
        self.addButton.setText(QCoreApplication.translate('QuantitiesDialog', 'Add'))
        self.editButtonLayout.addWidget(self.addButton)
        self.delButton = QToolButton(self)
        self.delButton.setText(QCoreApplication.translate('QuantitiesDialog', 'Delete'))
        self.editButtonLayout.addWidget(self.delButton)
        self.editButtonLayout.addStretch(100)
        self.connect(self.addButton, SIGNAL('pressed()'), self.newQuantity)
        self.connect(self.delButton, SIGNAL('pressed()'), self.delQuantities)


    def newQuantity(self):
        N = Text('Name', 'new_item', maxLen=100)
        D = Text('Description', '-empty-', maxLen=300)
        clsNames = quantityClasses.keys()
        T = Choice('Type', clsNames[0], choices=clsNames,
            descr=QCoreApplication.translate('QuantitiesDialog', 'Select type'))
        txt = QCoreApplication.translate('QuantitiesDialog', 'Select name, description and type')
        dlg = SimpleQuantitiesDialog(self, windowTitle=QCoreApplication.translate('QuantitiesDialog',
            'New Item'), text=txt, scrolling=False)
        dlg.addQuantities((N, D, T))
        if not dlg.exec_():
            return
        name = dlg.result[0].v
        while name in [q.name for q in self.quantityWidget.quantities if q]:
            name = name + 'X'
        descr = dlg.result[1].v
        cls = quantityClasses[dlg.result[2].v]
        if cls in [Choice, MultiChoice]:
            C = MLText('choices', '')
            txt = QCoreApplication.translate('QuantitiesDialog', 'Enter choices (one per line)')
            dlg = SimpleQuantitiesDialog(self, windowTitle=QCoreApplication.translate('QuantitiesDialog',
                'Choices'), text=txt, scrolling=False)
            dlg.addQuantities((C,))
            if dlg.exec_():
                choices = [c for c in dlg.result[0].v.split('\n') if c]
                self.quantityWidget.addQuantities((cls(name, descr=descr, choices=choices), ))
        else:
            self.quantityWidget.addQuantities((cls(name, descr=descr), ))


    def delQuantities(self):
        qnames = [q.name for q in self.quantityWidget.quantities if q is not None]
        Q = MultiChoice('Items', [], choices=qnames, descr=QCoreApplication.translate('QuantitiesDialog',
            'Quantities to delete'))
        txt = QCoreApplication.translate('QuantitiesDialog', 'Select items to delete')
        dlg = SimpleQuantitiesDialog(self, windowTitle=QCoreApplication.translate('QuantitiesDialog',
            'Delete items'), text=txt, scrolling=False)
        dlg.addQuantities((Q,))
        if dlg.exec_():
            delNames = dlg.result[0].v
            self.quantityWidget.delQuantities(*delNames)



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

