# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, Icons
from PyQt4.QtGui import QWizard, QWizardPage, QHBoxLayout, QVBoxLayout, QListWidget, QLabel,\
    QLineEdit, QFrame, QPixmap, QTextEdit
from PyQt4.QtCore import Qt, SIGNAL, QCoreApplication

SimTools = SimuVis4.Globals.plugInManager.getPlugIn('SimTools')
SQ = SimTools.Quantities



class ChartTemplate(object):
    """class to hold information on one type of chart: name, description, etc..."""
    def __init__(self):
        self.name = ''
        self.chartName = ''
        self.previewImage = None
        self.description = ''
        self.properties = []
        self.sensorInfo = {}
        self.sensors = {}

    def create(self, sensorgroup):
        #FXIME: add code here actually create the chart
        pass


class FooChart(ChartTemplate):
    def __init__(self):
        self.name = 'Carpet foo'
        self.chartName = 'FooCarpet'
        self.previewImage = None
        self.description = 'Foo carpet chart - Foo carpet chart - Foo carpet chart - Foo carpet chart'
        self.properties = [SQ.Integer('foo', 3), SQ.Float('bar', 4.0)]
        self.sensorInfo = {'bla': 1, 'fasel': 2}
        self.sensors = {}


class BarChart(ChartTemplate):
    def __init__(self):
        self.name = 'Carpet bar'
        self.chartName = 'BarCarpet'
        self.previewImage = None
        self.description = 'Bar carpet chart - Bar carpet chart - Bar carpet chart - Bar carpet chart'
        x = [("bla_%d" % i) for i in range(8)]
        self.properties = [SQ.Integer('bla', 3), SQ.Choice('fasel', x[0], choices=x)]
        self.sensorInfo = {'bla': 1, 'fasel': 2}
        self.sensors = {}



allChartTemplates = [FooChart(), BarChart()]



class NewChartPage0(QWizardPage):
    """WizardPage to select chart type and name"""
    def __init__(self, parent):
        QWizardPage.__init__(self, parent)
        self.setTitle(QCoreApplication.translate('DataStorageBrowser', 'Select type/template of chart'))
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        layout0 = QHBoxLayout()
        self.templateSelect = QListWidget(self)
        layout0.addWidget(self.templateSelect)
        self.templatePreview = QLabel(self)
        self.templatePreview.setMinimumSize(200, 200)
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
        for t in allChartTemplates:
            self.templateSelect.addItem(t.name)
        self.registerField('templateNumber', self.templateSelect, 'currentRow')
        self.registerField('chartName', self.nameInput, 'text')
        self.connect(self.templateSelect, SIGNAL("currentRowChanged(int)"), self.templateChanged)

    def templateChanged(self, i):
        t = allChartTemplates[i]
        self.templateInfo.setPlainText(t.description)
        if t.previewImage:
            self.templatePreview.setPixmap(QPixmap(t.previewImage))
        self.nameInput.setText(t.chartName)


class NewChartPage1(QWizardPage):
    """WizardPage to adjust chart properties"""
    def __init__(self, parent):
        QWizardPage.__init__(self, parent)
        self.setTitle(QCoreApplication.translate('DataStorageBrowser', 'Adjust chart properties'))
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.quantityWidget = None


    def initializePage(self):
        i, x = self.field('templateNumber').toInt()
        tmpl = allChartTemplates[i]
        if self.quantityWidget is not None:
            self.mainLayout.removeWidget(self.quantityWidget)
            self.quantityWidget.hide()
            del self.quantityWidget
        self.quantityWidget = SimTools.Widgets.QuantityWidget(self)
        self.mainLayout.addWidget(self.quantityWidget)
        self.quantityWidget.addQuantities(tmpl.properties)
        self.adjustSize()


class NewChartPage2(QWizardPage):
    """WizardPage to adjust attach sensors to chart"""
    def __init__(self, parent):
        QWizardPage.__init__(self, parent)
        self.setTitle(QCoreApplication.translate('DataStorageBrowser', 'Apply sensors to chart'))



class NewChartWizard(QWizard):

    def __init__(self, parent):
        QWizard.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('DataStorageBrowser', 'Add a new chart'))
        self.page0 = NewChartPage0(self)
        self.addPage(self.page0);
        self.page1 = NewChartPage1(self)
        self.addPage(self.page1);
        self.page2 = NewChartPage2(self)
        self.addPage(self.page2);



def showNewChartWizard(sensorgroup):
    wiz = NewChartWizard(SimuVis4.Globals.mainWin)
    wiz.exec_()
