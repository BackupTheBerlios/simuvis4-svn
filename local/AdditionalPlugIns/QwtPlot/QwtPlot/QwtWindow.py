# encoding: utf-8
# version:  $Id: VtkWindow.py 67 2007-11-17 18:25:01Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os
from SimuVis4.SubWin import SubWindow
from PyQt4.Qwt5 import QwtPlot, QwtLegend, QwtPlotGrid, QwtPlotZoomer, QwtPicker,\
    QwtPlotPrintFilter, QwtSlider, QwtPlotPanner, QwtPlotMagnifier
from PyQt4.QtGui import QFrame, QHBoxLayout, QToolButton, QSizePolicy, QPen, QPrinter,\
    QPrintDialog, QFileDialog, QDialog
from PyQt4.QtCore import SIGNAL, QCoreApplication, Qt, QSize
from PyQt4.QtSvg import QSvgGenerator

class QwtPlotWindow(SubWindow):
    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('QwtPlot', 'QwtPlotWindow'))
        self.plotWidget = QwtPlot(self)
        self.plotWidget.plotLayout().setAlignCanvasToScales(True)
        self.legend = QwtLegend()
        self.legend.setItemMode(QwtLegend.ClickableItem)
        self.plotWidget.insertLegend(self.legend, QwtPlot.RightLegend)
        self.grid = QwtPlotGrid()
        self.grid.attach(self.plotWidget)
        self.grid.setPen(QPen(Qt.black, 0, Qt.DotLine))
        self.zoomer = QwtPlotZoomer(QwtPlot.xBottom, QwtPlot.yLeft, QwtPicker.DragSelection,
            QwtPicker.AlwaysOff, self.plotWidget.canvas())
        self.zoomer.setRubberBandPen(QPen(Qt.green))
        self.magnifier = QwtPlotMagnifier(self.plotWidget.canvas())
        self.panner = QwtPlotPanner(self.plotWidget.canvas())
        self.panner.setMouseButton(Qt.LeftButton, Qt.ControlModifier)
        self.mainLayout.setMargin(0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.plotWidget, 1)
        self.setFocusProxy(self.plotWidget)
        self.resize(100, 100)
        self.setMinimumSize(200, 200)
        self.toolBar = None
        self.connect(self.plotWidget,SIGNAL("legendClicked(QwtPlotItem*)"), self.toggleVisibility)
        self.initToolBar()


    def toggleVisibility(self, plotItem):
        """Toggle the visibility of a plot item"""
        plotItem.setVisible(not plotItem.isVisible())
        self.plotWidget.replot()


    def initToolBar(self):
        if self.toolBar:
            return
        self.toolBar = QFrame(self)
        self.toolBarLayout = QHBoxLayout(self.toolBar)
        self.toolBarLayout.setMargin(4)
        self.toolBarLayout.setSpacing(4)

        self.zoomerButton = QToolButton(self.toolBar)
        self.zoomerButton.setText('Z')
        self.zoomerButton.setCheckable(True)
        self.zoomerButton.setChecked(self.zoomer.isEnabled())
        self.connect(self.zoomerButton, SIGNAL('toggled(bool)'), self.zoomer.setEnabled)
        self.toolBarLayout.addWidget(self.zoomerButton)

        self.magnifierButton = QToolButton(self.toolBar)
        self.magnifierButton.setText('M')
        self.magnifierButton.setCheckable(True)
        self.magnifierButton.setChecked(self.magnifier.isEnabled())
        self.connect(self.magnifierButton, SIGNAL('toggled(bool)'), self.magnifier.setEnabled)
        self.toolBarLayout.addWidget(self.magnifierButton)

        self.pannerButton = QToolButton(self.toolBar)
        self.pannerButton.setText('P')
        self.pannerButton.setCheckable(True)
        self.pannerButton.setChecked(self.panner.isEnabled())
        self.connect(self.magnifierButton, SIGNAL('toggled(bool)'), self.panner.setEnabled)
        self.toolBarLayout.addWidget(self.pannerButton)

        self.toolBarLayout.addSpacing(10)

        self.saveButton = QToolButton(self.toolBar)
        self.saveButton.setText('Save')
        self.toolBarLayout.addWidget(self.saveButton)
        self.connect(self.saveButton, SIGNAL('pressed()'), self.saveWindow)

        self.toolBarLayout.addStretch(100)
        self.mainLayout.addWidget(self.toolBar, 0)
        self.toolBar.show()


    def printWindow(self, printer=None):
        if not printer:
            printer = QPrinter()
        printer.setFullPage(True)
        printer.setPageSize(QPrinter.A4)
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle(QCoreApplication.translate('QwtPlot', 'Print Document'))
        if dialog.exec_() != QDialog.Accepted:
            return
        self.plotWidget.print_(printer, QwtPlotPrintFilter())


    def saveWindow(self):
        fileTypes = {'PDF':('pdf',), 'Postscript':('ps',),'SVG':('svg',)}
        filters = ';;'.join(['%s (%s)' % (k, ' '.join(['*.'+e for e in v])) for k, v in fileTypes.items()])
        dlg = QFileDialog(self,
            QCoreApplication.translate('QwtPlot', 'Select name of file to save'),
            SimuVis4.Globals.defaultFolder or '', filters)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        if dlg.exec_() != QDialog.Accepted:
            return
        tmp = str(dlg.selectedFilter())
        fileType = tmp[:tmp.find('(')-1]
        dlg.setDefaultSuffix(fileTypes[fileType][0])
        files = dlg.selectedFiles()
        if not files:
            return
        fileName = unicode(files[0])
        SimuVis4.Globals.defaultFolder, tmp = os.path.split(fileName)
        if fileType == 'PDF':
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOrientation(QPrinter.Landscape)
            printer.setOutputFileName(fileName)
            printer.setCreator('SimuVis4')
            self.plotWidget.print_(printer)
        elif fileType == 'Postscript':
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PostScriptFormat)
            printer.setOrientation(QPrinter.Landscape)
            printer.setOutputFileName(fileName)
            printer.setCreator('SimuVis4')
            self.plotWidget.print_(printer)
        elif fileType == 'SVG':
            generator = QSvgGenerator()
            generator.setFileName(fileName)
            generator.setSize(QSize(800, 600))
            self.plotWidget.print_(generator)
