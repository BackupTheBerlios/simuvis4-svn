# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os, sys

from PyQt4.QtGui import QFileDialog, QDialog, QWizard, QWizardPage, QSpinBox, QFileDialog, \
    QGridLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPixmap, QMessageBox
from PyQt4.QtCore import QCoreApplication, SIGNAL, QDateTime, Qt
from SimuVis4.Misc import uniqueName

from datastorage.importer.csvdata import CSVImporter
from datastorage.importer.remusdata import RemusImporter

class NewSensorgroupPage0(QWizardPage):
    """WizardPage to select sensorgroup name, title and importer"""
    def __init__(self, parent, project):
        QWizardPage.__init__(self, parent)
        self.setTitle(QCoreApplication.translate('DataStorageBrowser',
            'Select name, title and data type'))
        self.project = project
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        nameLabel = QLabel(self)
        nameLabel.setText('Name')
        self.mainLayout.addWidget(nameLabel, 0, 0)
        self.nameInput = QLineEdit(self)
        self.nameInput.setText(uniqueName('unnamed', project.keys()))
        self.registerField('name', self.nameInput, 'text')
        self.mainLayout.addWidget(self.nameInput, 0, 1)

        titleLabel = QLabel(self)
        titleLabel.setText('Title')
        self.mainLayout.addWidget(titleLabel, 1, 0)
        self.titleInput = QLineEdit(self)
        self.titleInput.setText('...')
        self.registerField('title', self.titleInput, 'text')
        self.mainLayout.addWidget(self.titleInput, 1, 1)

        typeLabel = QLabel(self)
        typeLabel.setText('Data type')
        self.mainLayout.addWidget(typeLabel, 2, 0)
        self.typeSelect = QComboBox(self)
        self.typeSelect.addItem('CSV')
        self.typeSelect.addItem('Remus')
        self.registerField('type', self.typeSelect, 'currentText')
        self.mainLayout.addWidget(self.typeSelect, 2, 1)


    def validatePage(self):
        n = str(self.field('name').toString())
        if not n:
            return False
        if n in self.project.keys():
            b = QMessageBox.question(self, QCoreApplication.translate('DataStorageBrowser',
                'Sensorgroup already exists!'), QCoreApplication.translate('DataStorageBrowser',
                'A sensorgroup with this name already exists. Do you really want to overwrite it?'),
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            return b == QMessageBox.Yes
        return True



class NewSensorgroupPage1(QWizardPage):
    """WizardPage to select constructor values"""
    def __init__(self, parent, project):
        QWizardPage.__init__(self, parent)
        self.setTitle(QCoreApplication.translate('DataStorageBrowser',
            'Select data import properties'))
        self.project = project
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        tsLabel = QLabel(self)
        tsLabel.setText('Time step')
        self.mainLayout.addWidget(tsLabel, 0, 0)
        self.tsInput = QSpinBox(self)
        self.tsInput.setSuffix(' s')
        self.tsInput.setSpecialValueText('---')
        self.tsInput.setMinimum(0)
        self.tsInput.setMaximum(86400)
        self.tsInput.setValue(0)
        self.registerField('timestep', self.tsInput, 'value')
        self.mainLayout.addWidget(self.tsInput, 0, 1)

        tzLabel = QLabel(self)
        tzLabel.setText('Time zone')
        self.mainLayout.addWidget(tzLabel, 1, 0)
        self.tzInput = QSpinBox(self)
        self.tzInput.setMinimum(0)
        self.tzInput.setMaximum(23)
        self.tzInput.setSuffix(' h')
        self.tzInput.setValue(0)
        self.registerField('timezone', self.tzInput, 'value')
        self.mainLayout.addWidget(self.tzInput, 1, 1)

        tfLabel = QLabel(self)
        tfLabel.setText('Time format')
        self.mainLayout.addWidget(tfLabel, 2, 0)
        self.tfInput = QLineEdit(self)
        self.tfInput.setText('')
        self.registerField('timeformat', self.tfInput, 'text')
        self.mainLayout.addWidget(self.tfInput, 2, 1)

        self.delimLabel = QLabel(self)
        self.delimLabel.setText('CSV separator')
        self.mainLayout.addWidget(self.delimLabel, 3, 0)
        self.delimInput = QLineEdit(self)
        self.delimInput.setMaxLength(1)
        self.delimInput.setText(';')
        self.registerField('delim', self.delimInput, 'text')
        self.mainLayout.addWidget(self.delimInput, 3, 1)

        self.tcolLabel = QLabel(self)
        self.tcolLabel.setText('CSV time column')
        self.mainLayout.addWidget(self.tcolLabel, 4, 0)
        self.tcolInput = QSpinBox(self)
        self.tcolInput.setMinimum(1)
        self.tcolInput.setMaximum(500)
        self.tcolInput.setValue(2)
        self.registerField('timecol', self.tcolInput, 'value')
        self.mainLayout.addWidget(self.tcolInput, 4, 1)

        self.extraLabel = QLabel(self)
        self.extraLabel.setText('CSV extra headers')
        self.mainLayout.addWidget(self.extraLabel, 5, 0)
        self.extraInput = QLineEdit(self)
        self.extraInput.setMaxLength(200)
        self.extraInput.setText('Device;Unit;SensorType')
        self.registerField('extra_headers', self.extraInput, 'text')
        self.mainLayout.addWidget(self.extraInput, 5, 1)


    def initializePage(self):
        t = str(self.field('type').toString())
        if t == 'CSV':
            self.tfInput.setText('%d.%m.%Y %H:%M')
            for w in (self.delimLabel, self.delimInput, self.tcolLabel, self.tcolInput,
                    self.extraLabel, self.extraInput):
                w.show()
        elif t == 'Remus':
            self.tfInput.setText('%d.%m.%y %H:%M:%S')
            for w in (self.delimLabel, self.delimInput, self.tcolLabel, self.tcolInput,
                    self.extraLabel, self.extraInput):
                w.hide()
        else:
            pass


    def validatePage(self):
        return True



class NewSensorgroupWizard(QWizard):

    def __init__(self, parent, project):
        QWizard.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('DataStorageBrowser',
            'Add a new sensorgroup'))
        self.addPage(NewSensorgroupPage0(self, project))
        self.addPage(NewSensorgroupPage1(self, project))



def newSensorGroup(model, mi):
    t, project = model.dsNode(mi)
    wiz = NewSensorgroupWizard(SimuVis4.Globals.mainWin, project)
    if not wiz.exec_():
        return
    # add sensorgroup
    name = str(wiz.field('name').toString())
    title = str(wiz.field('title').toString())
    sg = project.addGetSensorGroup(name, title)
    # set importer
    t = str(wiz.field('type').toString())
    timestep, x = wiz.field('timestep').toInt()
    if timestep == 0:
        timestep = None
    timezone, x = wiz.field('timezone').toInt()
    timeformat = str(wiz.field('timeformat').toString())
    print timestep, timezone, timeformat
    if t == 'Remus':
        imp = RemusImporter(tstep=timestep, tz=timezone, timefmt=timeformat)
        fileFilter = 'Remus (*.txt)'
    elif t == 'CSV':
        delim = str(wiz.field('delim').toString())
        timecol, x = wiz.field('timecol').toInt()
        extra_headers = str(wiz.field('extra_headers').toString()).split(delim)
        imp = CSVImporter(tstep=timestep, tz=timezone, timefmt=timeformat,
            delim=delim, timecol=timecol, extra_headers=extra_headers)
        fileFilter = 'CSV (*.csv *.txt)'
    else:
        return # should never happen
    sg.setImporter(imp)
    fileList = []
    tmp = QFileDialog.getOpenFileNames(SimuVis4.Globals.mainWin,
        QCoreApplication.translate('DataStorageBrowser', 'Select import data files'),
        SimuVis4.Globals.defaultFolder, fileFilter)
    fileList = [unicode(f) for f in tmp]
    if fileList:
        SimuVis4.Globals.defaultFolder, tmp = os.path.split(fileList[0])
        sg.syncFileList(fileList)
    model.addSensorgroup(mi, sg)



def importFiles(model, mi):
    t, sg = model.dsNode(mi)
    fileList = []
    tmp = QFileDialog.getOpenFileNames(SimuVis4.Globals.mainWin,
        QCoreApplication.translate('DataStorageBrowser', 'Select import data files'),
        SimuVis4.Globals.defaultFolder)
    fileList = [unicode(f) for f in tmp]
    if fileList:
        SimuVis4.Globals.defaultFolder, tmp = os.path.split(fileList[0])
        sg.syncFileList(fileList)

    sgItem = model.itemFromIndex(mi)

    # first delete all items
    rows = sgItem.rowCount()
    if rows > 0:
        sgItem.removeRows(0, rows)

    # and rebuild
    model._processSensorGroup(sg, sgItem, model.dsFolder(mi))
