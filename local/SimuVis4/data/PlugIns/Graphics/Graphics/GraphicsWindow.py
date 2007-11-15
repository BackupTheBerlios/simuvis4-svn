# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from SimuVis4.SubWin import SubWindow
from SimuVis4.Errors import IOError
import SimuVis4.Globals, os
from PyQt4.QtGui import QGraphicsView, QFileDialog, QPrintDialog, QDialog, QPrinter, QPainter, QMessageBox
from PyQt4.QtCore import SIGNAL, QCoreApplication, Qt, QRectF

from math import pow

helpText = QCoreApplication.translate('Graphics', \
"""Active keys in the Graphics window:
+/-/mousewheel: zoom in/out
r: reset view to original
m: maximize view
h: show this help
""")

class GraphicsWidget(QGraphicsView):
    """simple GraphicsView with mousewheel zooming
    mostly copied from elasticnodes.py"""
    def wheelEvent(self, event):
        self.scaleView(pow(2.0, -event.delta() / 240.0))

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)


class GraphicsWindow(SubWindow):
    """simple SubWindow with a QGraphicsView ready for painting"""

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        #self.graphicsView = QGraphicsView(self)
        self.graphicsView = GraphicsWidget(self)
        self.mainLayout.addWidget(self.graphicsView)
        self.setFocusProxy(self.graphicsView)
        self.graphicsView.setCacheMode(QGraphicsView.CacheBackground)
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.graphicsView.setRenderHint(QPainter.TextAntialiasing)
        self.resize(300, 300)

    def keyPressEvent(self, e):
        k = e.text()
        if k == '+':   self.graphicsView.scaleView(1.6)
        elif k == '-': self.graphicsView.scaleView(0.625)
        elif k == 'r': self.graphicsView.resetMatrix()
        elif k == 'm': self.graphicsView.fitInView(self.graphicsView.scene().itemsBoundingRect(), Qt.KeepAspectRatio)
        elif k == 'h':
            QMessageBox.information(SimuVis4.Globals.mainWin,
                QCoreApplication.translate('Graphics', 'Graphics window help'), helpText)
        SubWindow.keyPressEvent(self, e)

    def printWindow(self, printer=None):
        if not printer:
            printer = QPrinter()
        printer.setFullPage(True)
        printer.setPageSize(QPrinter.A4)
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle(QCoreApplication.translate('Graphics', 'Print Document'))
        if dialog.exec_() != QDialog.Accepted:
            return
        # FIXME: on windows the resolutions seems to be very low, why?
        #printer.setResolution(600)
        painter = QPainter(printer)
        painter.setRenderHint(QPainter.Antialiasing)
        self.graphicsView.scene().render(painter)
