# encoding: utf-8
# version:  $Id: Widgets.py 276 2008-01-14 17:28:08Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2

from PyQt4.QtGui import QDialog, QDialogButtonBox, QVBoxLayout, QGridLayout, QLabel, QLineEdit,\
    QComboBox, QSpinBox, QDoubleSpinBox, QWidget, QCheckBox, QScrollArea, QTextEdit,\
    QListWidget, QAbstractItemView, QDateTimeEdit, QHBoxLayout, QSizePolicy, QToolButton
from PyQt4.QtCore import QCoreApplication, SIGNAL, Qt, QObject, QDateTime

from RTypes import Text, MLText, Choice, MultiChoice, Float, Integer, Bool, DateTime


quantityClasses = {
    unicode(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Simple Text')): Text,
    unicode(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Multiline Text')): MLText,
    unicode(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Single Choice')): Choice,
    unicode(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Multiple Choice')): MultiChoice,
    unicode(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Boolean')): Bool,
    unicode(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Integer')): Integer,
    unicode(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Float')): Float,
    unicode(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Date+Time')): DateTime
}


class QuantityWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout = QGridLayout(self)
        self.quantities = []
        self.qwidgets   = []
        self.qlabels = []

    def addRichTypes(self, l):
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
                    w.setMaximumDate(maxdt.date())
            l.setBuddy(w)
            w.setToolTip(q.descr)
            w.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            w.adjustSize()
            self.gridLayout.addWidget(w, i, 1, 1, 1)
            self.qwidgets.append(w)
        self.adjustSize()


    def delRichTypes(self, *names):
        """delete RichTypes by name, widgets get disabled but not deleted"""
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



class SimpleRichTypesDialog(QDialog):
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

    def addRichTypes(self, l):
        """set the list of quantities"""
        self.quantityWidget.addRichTypes(l)

    def accept(self):
        """after dialog closes, quantity list is available as self.result"""
        self.result = self.quantityWidget.applyChanges()
        QDialog.accept(self)



class ComplexRichTypesDialog(SimpleRichTypesDialog):
    """complex dialog to display, change, add or delete quantities"""

    def __init__(self, parent=None, windowTitle='', scrolling=True, text=''):
        SimpleRichTypesDialog.__init__(self, parent, windowTitle, scrolling, text)
        self.editButtonLayout = QHBoxLayout()
        self.mainLayout.insertLayout(2, self.editButtonLayout)
        self.addButton = QToolButton(self)
        self.addButton.setText(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Add'))
        self.editButtonLayout.addWidget(self.addButton)
        self.delButton = QToolButton(self)
        self.delButton.setText(QCoreApplication.translate('RichTypes.Qt4Widgets', 'Delete'))
        self.editButtonLayout.addWidget(self.delButton)
        self.editButtonLayout.addStretch(100)
        self.connect(self.addButton, SIGNAL('pressed()'), self.newQuantity)
        self.connect(self.delButton, SIGNAL('pressed()'), self.delRichTypes)


    def newQuantity(self):
        N = Text('Name', 'new_item', maxLen=100)
        D = Text('Description', '-empty-', maxLen=300)
        clsNames = quantityClasses.keys()
        T = Choice('Type', clsNames[0], choices=clsNames,
            descr=QCoreApplication.translate('RichTypes.Qt4Widgets', 'Select type'))
        txt = QCoreApplication.translate('RichTypes.Qt4Widgets', 'Select name, description and type')
        dlg = SimpleRichTypesDialog(self, windowTitle=QCoreApplication.translate('RichTypes.Qt4Widgets',
            'New Item'), text=txt, scrolling=False)
        dlg.addRichTypes((N, D, T))
        if not dlg.exec_():
            return
        name = dlg.result[0].v
        while name in [q.name for q in self.quantityWidget.quantities if q]:
            name = name + 'X'
        descr = dlg.result[1].v
        cls = quantityClasses[dlg.result[2].v]
        if cls in (Choice, MultiChoice):
            C = MLText('choices', '')
            txt = QCoreApplication.translate('RichTypes.Qt4Widgets', 'Enter choices (one per line)')
            dlg = SimpleRichTypesDialog(self, windowTitle=QCoreApplication.translate('RichTypes.Qt4Widgets',
                'Choices'), text=txt, scrolling=False)
            dlg.addRichTypes((C,))
            if dlg.exec_():
                choices = [c for c in dlg.result[0].v.split('\n') if c]
                self.quantityWidget.addRichTypes((cls(name, descr=descr, choices=choices), ))
        elif cls == Float:
            # FIXME: adjust fMin, fMax
            fMin = -1e+10
            fMax =  1e+10
            MIN = Float('min', fMin, min=fMin, max=fMax)
            MAX = Float('max', fMax, min=fMin, max=fMax)
            STEP = Float('step', 1, min=0, max=fMax)
            txt = QCoreApplication.translate('RichTypes.Qt4Widgets', 'Enter properties')
            dlg = SimpleRichTypesDialog(self, windowTitle=QCoreApplication.translate('RichTypes.Qt4Widgets',
                'Properties'), text=txt, scrolling=False)
            dlg.addRichTypes((MIN, MAX, STEP))
            if dlg.exec_():
                self.quantityWidget.addRichTypes((Float(name, descr=descr, min=MIN.v, max=MAX.v, step=STEP.v), ))
        elif cls == Integer:
            # FIXME: adjust iMin, iMax
            iMin = -1e+5
            iMax =  1e+5
            MIN = Integer('min', iMin, min=iMin, max=iMax)
            MAX = Integer('max', iMax, min=iMin, max=iMax)
            STEP = Integer('step', 1, min=0, max=iMax)
            txt = QCoreApplication.translate('RichTypes.Qt4Widgets', 'Enter properties')
            dlg = SimpleRichTypesDialog(self, windowTitle=QCoreApplication.translate('RichTypes.Qt4Widgets',
                'Properties'), text=txt, scrolling=False)
            dlg.addRichTypes((MIN, MAX, STEP))
            if dlg.exec_():
                self.quantityWidget.addRichTypes((Integer(name, descr=descr, min=MIN.v, max=MAX.v, step=STEP.v), ))
        elif cls == DateTime:
            tMax = 2147483647
            MIN = DateTime('min', 0, min=0, max=tMax)
            MAX = DateTime('max', tMax, min=0, max=tMax)
            txt = QCoreApplication.translate('RichTypes.Qt4Widgets', 'Enter properties')
            dlg = SimpleRichTypesDialog(self, windowTitle=QCoreApplication.translate('RichTypes.Qt4Widgets',
                'Properties'), text=txt, scrolling=False)
            dlg.addRichTypes((MIN, MAX))
            if dlg.exec_():
                self.quantityWidget.addRichTypes((DateTime(name, descr=descr, min=MIN.v, max=MAX.v), ))
        elif cls in (Text, MLText):
            ML = Integer('maxLen', 1000, min=0, max=1e+5, step=1)
            txt = QCoreApplication.translate('RichTypes.Qt4Widgets', 'Enter properties')
            dlg = SimpleRichTypesDialog(self, windowTitle=QCoreApplication.translate('RichTypes.Qt4Widgets',
                'Properties'), text=txt, scrolling=False)
            dlg.addRichTypes((ML,))
            if dlg.exec_():
                self.quantityWidget.addRichTypes((cls(name, descr=descr, maxLen=ML.v), ))
        else:
            self.quantityWidget.addRichTypes((cls(name, descr=descr), ))


    def delRichTypes(self):
        qnames = [q.name for q in self.quantityWidget.quantities if q is not None]
        Q = MultiChoice('Items', [], choices=qnames, descr=QCoreApplication.translate('RichTypes.Qt4Widgets',
            'RichTypes to delete'))
        txt = QCoreApplication.translate('RichTypes.Qt4Widgets', 'Select items to delete')
        dlg = SimpleRichTypesDialog(self, windowTitle=QCoreApplication.translate('RichTypes.Qt4Widgets',
            'Delete items'), text=txt, scrolling=False)
        dlg.addRichTypes((Q,))
        if dlg.exec_():
            delNames = dlg.result[0].v
            self.quantityWidget.delRichTypes(*delNames)



def testDialogs():
    import time
    tmp = ['Entry '+str(i) for i in range(10)]
    rt = []
    rt.append(Text('text', 'default text', descr='some text', maxLen=15))
    rt.append(Choice('choice', tmp[4], descr='you choose!', choices=tmp))
    rt.append(Integer('int', 42, descr='integer number', min=39, max=50, step=3, unit='kWh'))
    rt.append(Float('float', 42.42, descr='float number'))
    rt.append(Bool('bool', True, descr='boolean value'))
    rt.append(MLText('mltext', 'default text\non two\nlines', descr='some multiline text'))
    rt.append(MultiChoice('mchoice', (tmp[3], tmp[7]), descr='choose one or more', choices=tmp))
    rt.append(DateTime('datetime', int(time.time()), descr='date and time'))
    txt = 'Test of RichTypes.Qt4Widgets.ComplexRichTypesDialog'
    dlg = ComplexRichTypesDialog(None, windowTitle='Complex Test', text=txt, scrolling=True)
    dlg.addRichTypes(rt)
    if dlg.exec_():
        rt = dlg.result
    txt = 'Test of RichTypes.Qt4Widgets.SimpleRichTypesDialog'
    dlg = SimpleRichTypesDialog(None, windowTitle='Simple Test', text=txt, scrolling=True)
    dlg.addRichTypes(rt)
    if dlg.exec_():
        rt = dlg.result



if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    testDialogs()
    #sys.exit(app.exec_())
