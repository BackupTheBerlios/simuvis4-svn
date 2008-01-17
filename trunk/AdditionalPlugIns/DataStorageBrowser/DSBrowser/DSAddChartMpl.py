# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, Icons, os
from PyQt4.QtGui import QWizard, QWizardPage, QHBoxLayout, QVBoxLayout, QListWidget, QLabel,\
    QLineEdit, QFrame, QPixmap, QTextEdit
from PyQt4.QtCore import Qt, SIGNAL, QCoreApplication
import DSChartTemplates

chartTemplates = DSChartTemplates.templateList[:]

SimTools = SimuVis4.Globals.plugInManager.getPlugIn('SimTools')

def reloadTemplates():
    global chartTemplates
    reload(DSChartTemplates)
    chartTemplates = DSChartTemplates.templateList[:]

    myself.getFile(os.path.join('previewImages', name)).read()



class NewChartPage0(QWizardPage):
    """WizardPage to select chart type and name"""
    def __init__(self, parent):
        QWizardPage.__init__(self, parent)
        self.setTitle(QCoreApplication.translate('DataStorageBrowser', 'Select type/template of chart'))
        self.setFinalPage(True)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        layout0 = QHBoxLayout()
        self.templateSelect = QListWidget(self)
        layout0.addWidget(self.templateSelect)
        self.templatePreview = QLabel(self)
        self.templatePreview.setScaledContents(True)
        self.templatePreview.setMinimumSize(200, 200)
        self.templatePreview.setMaximumSize(200, 200)
        self.templatePreview.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        layout0.addWidget(self.templatePreview)
        self.mainLayout.addLayout(layout0)
        self.templateInfo = QTextEdit(self)
        self.templateInfo.setReadOnly(True)
        self.templateInfo.setMinimumSize(400, 80)
        self.mainLayout.addWidget(self.templateInfo)
        layout1 = QHBoxLayout()
        nameLabel = QLabel(self)
        nameLabel.setText(QCoreApplication.translate('DataStorageBrowser', 'Chart name:'))
        layout1.addWidget(nameLabel)
        self.nameInput = QLineEdit(self)
        layout1.addWidget(self.nameInput)
        self.mainLayout.addLayout(layout1)
        for t in chartTemplates:
            self.templateSelect.addItem(t.name)
        self.registerField('templateNumber', self.templateSelect, 'currentRow')
        self.registerField('chartName', self.nameInput, 'text')
        self.ownPlugIn = SimuVis4.Globals.plugInManager['DataStorageBrowser']
        self.connect(self.templateSelect, SIGNAL("currentRowChanged(int)"), self.templateChanged)

    def templateChanged(self, i):
        t = chartTemplates[i]
        self.templateInfo.setPlainText(t.description)
        self.nameInput.setText(t.chartName)
        if t.previewImage:
            xpm = QPixmap()
            path = os.path.join('previewImages', t.previewImage)
            data = self.ownPlugIn.getFile(path).read()
            xpm.loadFromData(data)
            self.templatePreview.setPixmap(xpm)

    def validatePage(self):
        i, x = self.field('templateNumber').toInt()
        chartTemplates[i].chartName = str(self.field('chartName').toString())
        return True



class NewChartPage1(QWizardPage):
    """WizardPage to adjust chart properties"""
    def __init__(self, parent, sensorgroup):
        QWizardPage.__init__(self, parent)
        self.setTitle(QCoreApplication.translate('DataStorageBrowser', 'Adjust chart properties'))
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.quantityWidget = None
        self.sensorgroup = sensorgroup


    def initializePage(self):
        i, x = self.field('templateNumber').toInt()
        tmpl = chartTemplates[i]
        tmpl.setSensorgroup(self.sensorgroup)
        if self.quantityWidget is not None:
            self.mainLayout.removeWidget(self.quantityWidget)
            self.quantityWidget.hide()
            del self.quantityWidget
        self.quantityWidget = SimTools.Widgets.QuantityWidget(self)
        self.mainLayout.addWidget(self.quantityWidget)
        self.quantityWidget.addQuantities(tmpl.properties)
        self.adjustSize()



class NewChartWizard(QWizard):

    def __init__(self, parent, sensorgroup):
        QWizard.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('DataStorageBrowser', 'Add a new chart'))
        self.addPage(NewChartPage0(self))
        self.addPage(NewChartPage1(self, sensorgroup))



def showNewChartWizard(model, mi):
    t, sensorgroup = model.dsNode(mi)
    wiz = NewChartWizard(SimuVis4.Globals.mainWin, sensorgroup)
    wiz.sensorgroup = sensorgroup
    if not wiz.exec_():
        return
    i, x = wiz.field('templateNumber').toInt()
    template = chartTemplates[i]
    chart = template.makeChart(sensorgroup)
    model.addChart(chart, mi)
