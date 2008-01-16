# encoding: utf-8
# version:  $Id: VtkWindow.py 67 2007-11-17 18:25:01Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, os
from SimuVis4.SubWin import SubWindowV
from PyQt4.Qwt5 import QwtPlot, QwtLegend, QwtPlotGrid, QwtPlotZoomer, QwtPicker,\
    QwtPlotPrintFilter, QwtSlider, QwtPlotPanner, QwtPlotMagnifier, QwtPlotPicker
from PyQt4.QtGui import QFrame, QHBoxLayout, QToolButton, QSizePolicy, QPen, QPrinter,\
    QPrintDialog, QFileDialog, QDialog, QIcon, QPixmap, QLabel
from PyQt4.QtCore import SIGNAL, QCoreApplication, Qt, QSize
from PyQt4.QtSvg import QSvgGenerator


class QwtPlotE(QwtPlot):
    """a slightly enhanced version of QwtPlot which already has some sugar on it"""
    def __init__(self, *arg):
        QwtPlot.__init__(self, *arg)
        self.plotLayout().setAlignCanvasToScales(True)
        self.setCanvasBackground(Qt.white)
        self.legend = QwtLegend()
        self.legend.setItemMode(QwtLegend.ClickableItem)
        self.insertLegend(self.legend, QwtPlot.TopLegend)
        self.grid = QwtPlotGrid()
        self.grid.attach(self)
        self.grid.setPen(QPen(Qt.black, 0, Qt.DotLine))
        self.zoomer = QwtPlotZoomer(QwtPlot.xBottom, QwtPlot.yLeft, QwtPicker.DragSelection,
            QwtPicker.AlwaysOn, self.canvas())
        self.zoomer.setRubberBandPen(QPen(Qt.green))
        self.zoomer.setTrackerPen(QPen(Qt.red))
        self.magnifier = QwtPlotMagnifier(self.canvas())
        self.panner = QwtPlotPanner(self.canvas())
        self.panner.setMouseButton(Qt.LeftButton, Qt.ControlModifier)
        self.connect(self, SIGNAL("legendClicked(QwtPlotItem*)"), self.togglePlotItemVisibility)

    def togglePlotItemVisibility(self, plotItem):
        """Toggle the visibility of a plot item"""
        plotItem.setVisible(not plotItem.isVisible())
        self.replot()



class QwtPlotWindow(SubWindowV):
    def __init__(self, parent, plotClass=QwtPlotE, *args):
        SubWindowV.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('QwtPlot', 'QwtPlotWindow'))
        self.plot = plotClass(self, *args)
        self.mainLayout.setMargin(0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.plot, 1)
        self.setFocusProxy(self.plot)
        self.resize(100, 100)
        self.setMinimumSize(350, 200)
        self.toolBar = None
        self.initToolBar()


    def initToolBar(self):
        if self.toolBar:
            return
        self.toolBar = QFrame(self)
        self.toolBarLayout = QHBoxLayout(self.toolBar)
        self.toolBarLayout.setMargin(4)
        self.toolBarLayout.setSpacing(2)

        self.saveButton = QToolButton(self.toolBar)
        self.saveButton.setText(QCoreApplication.translate('QwtPlot', 'Save...'))
        self.saveButton.setIcon(QIcon(QPixmap(SimuVis4.Icons.fileSave)))
        self.saveButton.setToolTip(QCoreApplication.translate('QwtPlot', 'Save plot as graphics'))
        self.toolBarLayout.addWidget(self.saveButton)
        self.connect(self.saveButton, SIGNAL('pressed()'), self.saveWindow)

        self.printButton = QToolButton(self.toolBar)
        self.printButton.setText(QCoreApplication.translate('QwtPlot', 'Print...'))
        self.printButton.setIcon(QIcon(QPixmap(SimuVis4.Icons.filePrint)))
        self.printButton.setToolTip(QCoreApplication.translate('QwtPlot', 'Print plot to printer or file'))
        self.toolBarLayout.addWidget(self.printButton)
        self.connect(self.printButton, SIGNAL('pressed()'), self.printWindow)

        self.toolBarLayout.addSpacing(10)

        if hasattr(self.plot, 'zoomer'):
            self.zoomerButton = QToolButton(self.toolBar)
            self.zoomerButton.setText('Z')
            self.zoomerButton.setIcon(QIcon(QPixmap(SimuVis4.Icons.zoom)))
            self.zoomerButton.setToolTip(QCoreApplication.translate('QwtPlot', 'Enable zooming with the mouse'))
            self.zoomerButton.setCheckable(True)
            self.zoomerButton.setChecked(self.plot.zoomer.isEnabled())
            self.connect(self.zoomerButton, SIGNAL('toggled(bool)'), self.plot.zoomer.setEnabled)
            self.toolBarLayout.addWidget(self.zoomerButton)

        if hasattr(self.plot, 'magnifier'):
            self.magnifierButton = QToolButton(self.toolBar)
            self.magnifierButton.setText('M')
            self.magnifierButton.setIcon(QIcon(QPixmap(SimuVis4.Icons.magnify)))
            self.magnifierButton.setToolTip(QCoreApplication.translate('QwtPlot', 'Enable magnifying with the mouse'))
            self.magnifierButton.setCheckable(True)
            self.magnifierButton.setChecked(self.plot.magnifier.isEnabled())
            self.connect(self.magnifierButton, SIGNAL('toggled(bool)'), self.plot.magnifier.setEnabled)
            self.toolBarLayout.addWidget(self.magnifierButton)

        if hasattr(self.plot, 'panner'):
            self.pannerButton = QToolButton(self.toolBar)
            self.pannerButton.setText('P')
            self.pannerButton.setIcon(QIcon(QPixmap(SimuVis4.Icons.pan)))
            self.pannerButton.setToolTip(QCoreApplication.translate('QwtPlot', 'Enable panning with the mouse'))
            self.pannerButton.setCheckable(True)
            self.pannerButton.setChecked(self.plot.panner.isEnabled())
            self.connect(self.magnifierButton, SIGNAL('toggled(bool)'), self.plot.panner.setEnabled)
            self.toolBarLayout.addWidget(self.pannerButton)

            self.toolBarLayout.addSpacing(10)

        self.statusLabel = QLabel(self.toolBar)
        self.toolBarLayout.addWidget(self.statusLabel)

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
        self.plot.print_(printer, QwtPlotPrintFilter())


    def saveWindow(self):
        fileTypes = {'PDF':('pdf',), 'Postscript':('ps',),'SVG':('svg',)}
        filters = ';;'.join(['%s (%s)' % (k, ' '.join(['*.'+e for e in v])) for k, v in fileTypes.items()])
        dlg = QFileDialog(self,
            QCoreApplication.translate('QwtPlot', 'Select type and name of file to save'),
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
            self.plot.print_(printer)
        elif fileType == 'Postscript':
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PostScriptFormat)
            printer.setOrientation(QPrinter.Landscape)
            printer.setOutputFileName(fileName)
            printer.setCreator('SimuVis4')
            self.plot.print_(printer)
        elif fileType == 'SVG':
            generator = QSvgGenerator()
            generator.setFileName(fileName)
            generator.setSize(QSize(800, 600))
            self.plot.print_(generator)
