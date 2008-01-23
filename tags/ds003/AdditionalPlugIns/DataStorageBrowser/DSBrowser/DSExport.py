# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os, string

from PyQt4.QtGui import QFileDialog, QDialog, QAbstractItemView, QDesktopServices
from PyQt4.QtCore import QCoreApplication, SIGNAL, QDateTime, Qt, QUrl

from UI.DSExportDialog import Ui_DSExportDialog

from datastorage.sensorgroup import hasExelerator
from datastorage.timegrid import TimeGrid

from time import strftime, gmtime

epoch = gmtime(0)

infoTxt = string.Template(unicode(QCoreApplication.translate('DataStorageBrowser', """
<b>Export file format:</b> $format<br/>
<b>Sensors (columns):</b> $sensors<br/>
<b>Time steps (rows):</b> $timesteps<br/>
<b>Values (total):</b> $values<br/>
<b>File size:</b> $filesize (raw guess)<br/>
<font color="#ff0000">$warning</font>
""")))


class ExportDialog(QDialog, Ui_DSExportDialog):

    def __init__(self, parent, sg):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(str(QCoreApplication.translate('DataStorageBrowser',
            'Data export from %s')) % sg.path)
        self.sensorgroup = sg
        self.connect(self, SIGNAL('accepted()'), self.exportData)

        self.connect(self.fileNameButton, SIGNAL('clicked()'), self.changeFileName)
        self.fileName = os.path.join(SimuVis4.Globals.defaultFolder, sg.name+'.csv')
        while os.path.exists(self.fileName):
            self.fileName = self.fileName[:-4]+'_X.csv'
        self.fileNameInput.setText(self.fileName)
        self.fileType='CSV'

        self.sensorList.setSelectionMode(QAbstractItemView.MultiSelection)
        for i, s in enumerate(sg.keys()):
            self.sensorList.addItem(s)
            self.sensorList.item(i).setSelected(True)
        self.connect(self.sensorList, SIGNAL('itemSelectionChanged()'), self.showInfo)

        self.connect(self.startInput, SIGNAL('dateTimeChanged(QDateTime)'), self.startTimeChanged)
        self.connect(self.stopInput, SIGNAL('dateTimeChanged(QDateTime)'), self.stopTimeChanged)
        self.startTime = sg.start
        self.stopTime = sg.stop
        mindt = QDateTime()
        mindt.setTimeSpec(Qt.UTC)
        mindt.setTime_t(self.startTime)
        maxdt = QDateTime()
        mindt.setTimeSpec(Qt.UTC)
        maxdt.setTime_t(self.stopTime)
        self.startInput.setMinimumDate(mindt.date())
        self.startInput.setMaximumDate(maxdt.date())
        self.stopInput.setMinimumDate(mindt.date())
        self.stopInput.setMaximumDate(maxdt.date())
        self.startInput.setDateTime(mindt)
        self.stopInput.setDateTime(maxdt)


    def changeFileName(self):
        fileTypes = {'CSV':('csv',) }
        if hasExelerator:
            fileTypes['MS Excel'] = ('xls',)
        filters = ';;'.join(['%s (%s)' % (k, ' '.join(['*.'+e for e in v])) for k, v in fileTypes.items()])
        dlg = QFileDialog(self,
            QCoreApplication.translate('DataStorageBrowser', 'Select name of file to save'),
            SimuVis4.Globals.defaultFolder or '', filters)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.selectFile(os.path.split(self.fileName)[-1])
        if dlg.exec_() != QDialog.Accepted:
            return
        tmp = str(dlg.selectedFilter())
        self.fileType = tmp[:tmp.find('(')-1]
        dlg.setDefaultSuffix(fileTypes[self.fileType][0])
        files = dlg.selectedFiles()
        if not files:
            return
        self.fileName = unicode(files[0])
        self.fileNameInput.setText(self.fileName)
        SimuVis4.Globals.defaultFolder, tmp = os.path.split(self.fileName)
        if self.fileType == 'CSV':
            self.separatorLabel.setEnabled(True)
            self.separatorInput.setEnabled(True)
            self.separatorInfoLabel.setEnabled(True)
        else:
            self.separatorLabel.setEnabled(False)
            self.separatorInput.setEnabled(False)
            self.separatorInfoLabel.setEnabled(False)
        self.showInfo()


    def startTimeChanged(self, dt):
        dt.setTimeSpec(Qt.UTC)
        self.startTime = self.sensorgroup.timegrid.moveOnGrid(dt.toTime_t(), TimeGrid.nearest)
        self.showInfo()


    def stopTimeChanged(self, dt):
        dt.setTimeSpec(Qt.UTC)
        self.stopTime = self.sensorgroup.timegrid.moveOnGrid(dt.toTime_t(), TimeGrid.nearest)
        self.showInfo()


    def showInfo(self, *arg):
        sizeFactor = {'CSV' : 5, 'MS Excel' : 15}
        sensors = len(self.sensorList.selectedIndexes())
        timesteps = int((self.stopTime - self.startTime)/self.sensorgroup.step)
        tmp = sensors*timesteps * sizeFactor[self.fileType]
        if tmp > 1000000:
            filesize = '%.1f MB' % (tmp*1.0e-6)
        elif tmp > 1000:
            filesize = '%.1f KB' % (tmp*1.0e-3)
        else:
            filesize = '%s B' % tmp
        warning = ''
        if self.fileType == 'MS Excel':
            if sensors > 256 or timesteps > 65534:
                warning = str(QCoreApplication.translate('DataStorageBrowser',
                    '<b>To many values in Excel file:</b><br>65534 rows and 256 columns max.!'))
        txt = infoTxt.substitute(format=self.fileType, sensors=sensors,
            timesteps=timesteps, values=sensors*timesteps, filesize=filesize, warning=warning)
        self.infoLabel.setText(txt)


    def exportData(self):
        startTuple = self.sensorgroup.timegrid.gmt2tupletz(self.startTime)
        stopTuple = self.sensorgroup.timegrid.gmt2tupletz(self.stopTime)
        slc =  slice(startTuple, stopTuple)
        sensors = [unicode(i.text()) for i in self.sensorList.selectedItems()]
        if self.fileType == 'CSV':
            sep = str(self.separatorInput.text())
            self.sensorgroup.exportCSV(slc, self.fileName, sensors, sep)
        elif self.fileType == 'MS Excel':
            # FIXME: sensorlist?
            self.sensorgroup.exportEXCEL(slc, self.fileName)
        if self.openFileButton.isChecked():
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.fileName))



def exportSensors(node):
    ExportDialog(SimuVis4.Globals.mainWin, node).exec_()
