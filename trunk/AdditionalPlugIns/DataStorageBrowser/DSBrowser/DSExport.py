# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os, string

from PyQt4.QtGui import QFileDialog, QDialog, QAbstractItemView
from PyQt4.QtCore import QCoreApplication, SIGNAL, QDateTime

from UI.DSExportDialog import Ui_DSExportDialog

from datastorage.sensorgroup import hasExelerator

from time import strftime, gmtime

def timeStr(t):
    return strftime('%d.%m.%Y - %H:%M', gmtime(t))


infoTxt = string.Template(unicode(QCoreApplication.translate('DataStorageBrowser', """
<b>Export file format:</b> $format<br/>
<b>Sensors (columns):</b> $sensors<br/>
<b>Timesteps (rows):</b> $timesteps<br/>
<b>Values:</b> $values<br/>
<b>File size:</b> $filesize (raw guess)<br/>
<b>$warning</b>
""")))


class ExportDialog(QDialog, Ui_DSExportDialog):

    def __init__(self, parent, sg):
        QDialog.__init__(self, parent)
        self.setupUi(self)
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

        self.connect(self.startInput, SIGNAL('valueChanged(int)'), self.startValueChanged)
        self.connect(self.stopInput, SIGNAL('valueChanged(int)'), self.stopValueChanged)
        nValues = sg.timegrid.dataLen()
        self.startInput.setMinimum(0)
        self.startInput.setMaximum(nValues-2)
        self.stopInput.setMinimum(1)
        self.stopInput.setMaximum(nValues-1)
        self.startInput.setValue(0)
        self.stopInput.setValue(nValues-1)


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
        self.showInfo()


    def startValueChanged(self, i):
        self.startInfoLabel.setText(timeStr(self.sensorgroup.timegrid.indexToTime(i)))
        self.showInfo()


    def stopValueChanged(self, i):
        self.stopInfoLabel.setText(timeStr(self.sensorgroup.timegrid.indexToTime(i)))
        self.showInfo()


    def showInfo(self, *arg):
        sizeFactor = {'CSV' : 5, 'MS Excel' : 15}
        sensors = len(self.sensorList.selectedIndexes())
        timesteps=self.stopInput.value()-self.startInput.value()
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
                warning = """<font color="#ff0000"><b>To many values in Excel file:</b><br>
                65534 rows and 256 columns max.!</font>"""
        txt = infoTxt.substitute(format=self.fileType, sensors=sensors,
            timesteps=timesteps, values=sensors*timesteps, filesize=filesize, warning=warning)
        self.infoLabel.setText(txt)


    def exportData(self):
        # FIXME: does not work! Why?
        #slc =  slice(self.startInput.value(), self.stopInput.value(), None)
        slc =  slice(None, None, None)
        sensors = [unicode(i.text()) for i in self.sensorList.selectedItems()]
        if self.fileType == 'CSV':
            sep = str(self.separatorInput.text())
            self.sensorgroup.exportCSV(slc, self.fileName, sensors, sep)
        elif self.fileType == 'MS Excel':
            # FIXME: sensorlist?
            self.sensorgroup.exportEXCEL(slc, self.fileName)



def exportSensors(node):
    ExportDialog(SimuVis4.Globals.mainWin, node).exec_()
