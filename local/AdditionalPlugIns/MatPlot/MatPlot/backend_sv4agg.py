# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""
Render to SimuVis4 from agg

This is heavily based on backend_qt4 and backend_qt4agg with only
small changes.
"""
from __future__ import division

import math, os, sys, tempfile

import matplotlib
from matplotlib import verbose
from matplotlib.numerix import asarray, fromstring, UInt8, zeros, \
     where, transpose, nonzero, indices, ones, nx
import matplotlib.numerix as numerix
from matplotlib.cbook import is_string_like, enumerate, onetrue
from matplotlib.font_manager import fontManager
from matplotlib.backend_bases import RendererBase, GraphicsContextBase, \
     FigureManagerBase, FigureCanvasBase, NavigationToolbar2, cursors
from matplotlib._pylab_helpers import Gcf
from matplotlib.figure import Figure
from matplotlib.mathtext import math_parse_s_ft2font
from matplotlib.widgets import SubplotTool
try:
    from backend_agg import FigureCanvasAgg
    from backend_qt4 import SubplotToolQt
except ImportError:
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.backends.backend_qt4 import SubplotToolQt


try:
    import SimuVis4
    import SimuVis4.Globals
    from SimuVis4.SubWin import SubWindow, SubWindowV
    mainWin = SimuVis4.Globals.mainWin
except:
    raise "This backend works only from SimuVis4!"

from PyQt4 import QtCore, QtGui


backend_version = "0.2.0"

imagepath = matplotlib.rcParams['datapath']
tmp = os.path.join(imagepath, 'images')
if os.path.isdir(tmp):
    imagepath = tmp

cursord = {
    cursors.MOVE          : QtCore.Qt.PointingHandCursor,
    cursors.HAND          : QtCore.Qt.WaitCursor,
    cursors.POINTER       : QtCore.Qt.ArrowCursor,
    cursors.SELECT_REGION : QtCore.Qt.CrossCursor,
    }

def draw_if_interactive():
    """
    Is called after every pylab drawing command
    """
    if matplotlib.is_interactive():
        figManager =  Gcf.get_active()
        if figManager != None:
            figManager.canvas.draw()

def show():
    """ Show all the figures """
    for manager in Gcf.get_all_fig_managers():
        manager.window.show()
    figManager =  Gcf.get_active()
    if figManager != None:
        figManager.canvas.draw()

def new_figure_manager( num, *args, **kwargs ):
    """ Create a new figure manager instance """
    FigureClass = kwargs.pop('FigureClass', Figure)
    thisFig = FigureClass( *args, **kwargs )
    canvas = FigureCanvasSV4( thisFig )
    return FigureManagerSV4( canvas, num )


class MatPlotWindow(SubWindowV):
    def setup(self, canvas, num):
        mainWin.workSpace.addSubWindow(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.mainLayout.setSpacing(2)

        self.setWindowTitle(unicode(QtCore.QCoreApplication.translate('MatPlot', 'Figure %d')) % num)
        image = os.path.join(imagepath,'matplotlib.png')
        self.setWindowIcon(QtGui.QIcon(image))

        self.canvas = canvas
        canvas.setParent(self)
        canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        canvas.setFocus()
        self.mainLayout.addWidget(canvas, 1)
        self.setMinimumSize(350, 300)


    def printWindow(self, printer=None):
        # printing is done via SVG in a temporary file
        try:
            self.canvas.print_dialog(printer)
        except ImportError:
            SubWindow.printWindow(self, printer)
            return


    def saveWindow(self, fileName=None):
        self.toolbar.save_figure()


class FigureManagerSV4( FigureManagerBase ):
    """
    Public attributes

    canvas      : The FigureCanvas instance
    num         : The Figure number
    toolbar     : The qt.QToolBar
    window      : The qt.QMainWindow 
    """

    def __init__( self, canvas, num ):
        FigureManagerBase.__init__( self, canvas, num )
        self.canvas = canvas

        window = MatPlotWindow(mainWin.workSpace)
        window.setup(canvas, num)
        self.window = window


        QtCore.QObject.connect(window, QtCore.SIGNAL( 'destroyed()' ),
                            self._widgetclosed )
        window._destroying = False

        toolbar = self._get_toolbar(canvas, window)
        window.toolbar = toolbar
        self.toolbar = toolbar
        if toolbar:
           window.mainLayout.addWidget(toolbar, 0)

        window.resize(640, 480)

        if matplotlib.is_interactive():
            window.setMinimumSize(200, 200)
            window.show()

        def notify_axes_change( fig ):
           # This will be called whenever the current axes is changed
           if self.toolbar != None: self.toolbar.update()
           self.canvas.figure.add_axobserver( notify_axes_change )

    def _widgetclosed( self ):
        if self.window._destroying: return
        self.window._destroying = True
        Gcf.destroy(self.num)

    def _get_toolbar(self, canvas, parent):
        # must be inited after the window, drawingArea and figure
        # attrs are set
        if matplotlib.rcParams['toolbar'] == 'classic':
            print "Classic toolbar is not yet supported"
        elif matplotlib.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2SV4(canvas, parent)
        else:
            toolbar = None
        return toolbar

    def resize(self, width, height):
        """set the canvas size in pixels"""
        self.window.resize(width, height)

    def destroy( self, *args ):
        if self.window._destroying: return
        self.window._destroying = True
        self.window.close()


class NavigationToolbar2SV4( NavigationToolbar2, QtGui.QWidget ):
    # list of toolitems to add to the toolbar, format is:
    # text, tooltip_text, image_file, callback(str)
    toolitems = (
        (QtCore.QCoreApplication.translate('MatPlot', 'Home'),
            QtCore.QCoreApplication.translate('MatPlot', 'Reset original view'),
            'home.png', 'home'),
        (QtCore.QCoreApplication.translate('MatPlot', 'Back'),
            QtCore.QCoreApplication.translate('MatPlot', 'Back to  previous view'),
            'back.png', 'back'),
        (QtCore.QCoreApplication.translate('MatPlot', 'Forward'),
            QtCore.QCoreApplication.translate('MatPlot', 'Forward to next view'),
            'forward.png', 'forward'),
        (None, None, None, None),        
        (QtCore.QCoreApplication.translate('MatPlot', 'Pan'),
            QtCore.QCoreApplication.translate('MatPlot', 'Pan axes with left mouse, zoom with right'),
            'move.png', 'pan'),
        (QtCore.QCoreApplication.translate('MatPlot', 'Zoom'),
            QtCore.QCoreApplication.translate('MatPlot', 'Zoom to rectangle'),
            'zoom_to_rect.png', 'zoom'),
        (None, None, None, None),
        (QtCore.QCoreApplication.translate('MatPlot', 'Subplots'),
            QtCore.QCoreApplication.translate('MatPlot', 'Configure subplots'),
            'subplots.png', 'configure_subplots'),
        (QtCore.QCoreApplication.translate('MatPlot', 'Save'),
            QtCore.QCoreApplication.translate('MatPlot', 'Save the figure'),
            'filesave.png', 'save_figure'),
    )

    def __init__(self, canvas, parent):
        self.canvas = canvas
        QtGui.QWidget.__init__(self, parent)

        # Layout toolbar buttons horizontally.
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.setMargin(0)
        self.layout.setSpacing(0)

        NavigationToolbar2.__init__( self, canvas )

    def _init_toolbar(self):
        for text, tooltip_text, image_file, callback in self.toolitems:
            if not text:
                self.layout.addSpacing(8)
                continue
            image = QtGui.QPixmap()
            image.load(os.path.join(imagepath, image_file))
            button = QtGui.QToolButton(self)
            button.setText(text)
            button.setIcon(QtGui.QIcon(image))
            button.setToolTip(tooltip_text)
            QtCore.QObject.connect( button, QtCore.SIGNAL('clicked()'), getattr(self, callback))
            self.layout.addWidget(button)

        printButton = QtGui.QToolButton(self)
        printButton.setText(QtCore.QCoreApplication.translate('MatPlot', 'Print'))
        printButton.setIcon(QtGui.QIcon(QtGui.QPixmap(SimuVis4.Icons.filePrint)))
        printButton.setToolTip(QtCore.QCoreApplication.translate('MatPlot', 'Print the figure'))
        QtCore.QObject.connect(printButton, QtCore.SIGNAL('clicked()'), self.print_dialog)
        self.layout.addWidget(printButton)

        self.locLabel = QtGui.QLabel(self)
        self.locLabel.setAlignment( QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter )
        self.locLabel.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored,
                                                      QtGui.QSizePolicy.Ignored))
        self.layout.addWidget(self.locLabel, 1)

    def dynamic_update(self):
        self.canvas.draw()

    def set_message( self, s ):
        self.locLabel.setText(s)

    def set_cursor( self, cursor ):
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QApplication.setOverrideCursor( QtGui.QCursor( cursord[cursor] ) )

    def draw_rubberband( self, event, x0, y0, x1, y1 ):
        height = self.canvas.figure.bbox.height()
        y1 = height - y1
        y0 = height - y0

        w = abs(x1 - x0)
        h = abs(y1 - y0)

        rect = [ int(val)for val in min(x0,x1), min(y0, y1), w, h ]
        self.canvas.drawRectangle( rect )

    def configure_subplots(self):
        win = SubWindow(mainWin.workSpace)
        mainWin.workSpace.addSubWindow(win)
        win.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        win.setWindowTitle(QtCore.QCoreApplication.translate('MatPlot', 'Subplot Configuration Tool'))
        image = os.path.join(imagepath,'matplotlib.png' )
        win.setWindowIcon(QtGui.QIcon(image))
        tool = SubplotToolQt(self.canvas.figure, win)
        win.setWidget(tool)
        win.setMinimumSize(300, 200)
        win.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        win.show()

    def _get_canvas(self, fig):
        return FigureCanvasSV4(fig)

    def save_figure(self):
        fileTypes = {'PNG':('png',), 'PS':('ps',), 'EPS':('eps',), 'BMP':('bmp',), 'SVG':('svg',), 'PDF':('pdf',)}
        filters = ';;'.join(['%s (%s)' % (k, ' '.join(['*.'+e for e in v])) for k, v in fileTypes.items()])
        dlg = QtGui.QFileDialog(self,
            QtCore.QCoreApplication.translate('MatPlot', 'Select file to save'),
            SimuVis4.Globals.defaultFolder or '', filters)
        dlg.setFileMode(QtGui.QFileDialog.AnyFile)
        dlg.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        if dlg.exec_() != QtGui.QDialog.Accepted:
            return
        tmp = str(dlg.selectedFilter())
        fileType = tmp[:tmp.find('(')-1]
        dlg.setDefaultSuffix(fileTypes[fileType][0])
        files = dlg.selectedFiles()
        if not files:
            return
        fileName = unicode(files[0])
        SimuVis4.Globals.defaultFolder, tmp = os.path.split(fileName)
        self.canvas.print_figure(fileName, dpi=300)

    def print_dialog(self):
        self.canvas.print_dialog()


class FigureCanvasSV4(QtGui.QWidget, FigureCanvasAgg ):
    keyvald = { QtCore.Qt.Key_Control : 'control',
                QtCore.Qt.Key_Shift : 'shift',
                QtCore.Qt.Key_Alt : 'alt',
               }
    # left 1, middle 2, right 3
    buttond = {1:1, 2:3, 4:2}
    def __init__( self, figure ):

        QtGui.QWidget.__init__( self )
        FigureCanvasAgg.__init__( self, figure )
        self.figure = figure
        self.setMouseTracking( True )

        w,h = self.get_width_height()
        self.resize( w, h )
        self.drawRect = False
        self.rect = []
        self.replot = True
        self.pixmap = QtGui.QPixmap()

    def mousePressEvent( self, event ):
        x = event.pos().x()
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height() - event.pos().y()
        button = self.buttond[event.button()]
        FigureCanvasAgg.button_press_event( self, x, y, button )

    def mouseMoveEvent( self, event ):
        x = event.x()
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height() - event.y()
        FigureCanvasAgg.motion_notify_event( self, x, y )

    def mouseReleaseEvent( self, event ):
        x = event.x()
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height() - event.y()
        button = self.buttond[event.button()]
        FigureCanvasAgg.button_release_event( self, x, y, button )
        self.draw()

    def keyPressEvent( self, event ):
        key = self._get_key( event )
        FigureCanvasAgg.key_press_event(self, key )

    def keyReleaseEvent( self, event ):
        key = self._get_key(event)
        FigureCanvasAgg.key_release_event( self, key )

    def resizeEvent( self, e ):
        QtGui.QWidget.resizeEvent( self, e)
        w = e.size().width()
        h = e.size().height()
        dpival = self.figure.dpi.get()
        winch = w/dpival
        hinch = h/dpival
        self.figure.set_size_inches( winch, hinch )
        self.draw()

    def resize( self, w, h ):
        QtGui.QWidget.resize( self, w, h )

    def drawRectangle( self, rect ):
        self.rect = rect
        self.drawRect = True
        self.repaint( )

    def paintEvent( self, e ):
        """
        Draw to the Agg backend and then copy the image to the qt.drawable.
        In Qt, all drawing should be done inside of here when a widget is
        shown onscreen.
        """
        p = QtGui.QPainter( self )

        # only replot data when needed
        if type(self.replot) is bool: # might be a bbox for blitting
            if (self.replot ):
                #stringBuffer = str( self.buffer_rgba(0,0) )
                FigureCanvasAgg.draw( self )

                # matplotlib is in rgba byte order.
                # qImage wants to put the bytes into argb format and
                # is in a 4 byte unsigned int.  little endian system is LSB first
                # and expects the bytes in reverse order (bgra).
                if ( QtCore.QSysInfo.ByteOrder == QtCore.QSysInfo.LittleEndian ):
                    stringBuffer = self.renderer._renderer.tostring_bgra()
                else:
                    stringBuffer = self.renderer._renderer.tostring_argb()
                qImage = QtGui.QImage(stringBuffer, self.renderer.width,
                                       self.renderer.height,
                                       QtGui.QImage.Format_ARGB32)
                self.pixmap = self.pixmap.fromImage( qImage )
            p.drawPixmap( QtCore.QPoint( 0, 0 ), self.pixmap )

            # draw the zoom rectangle to the QPainter
            if ( self.drawRect ):
                p.setPen( QtGui.QPen( QtCore.Qt.black, 1, QtCore.Qt.DotLine ) )
                p.drawRect( self.rect[0], self.rect[1], self.rect[2], self.rect[3] )

        # we are blitting here
        else:
            bbox = self.replot
            w, h = int(bbox.width()), int(bbox.height())
            l, t = bbox.ll().x().get(), bbox.ur().y().get()
            reg = self.copy_from_bbox(bbox)
            stringBuffer = reg.to_string()
            qImage = QtGui.QImage(stringBuffer, w, h, QtGui.QImage.Format_ARGB32)
            self.pixmap = self.pixmap.fromImage( qImage )
            p.drawPixmap(QtCore.QPoint(l, self.renderer.height-t), self.pixmap)

        p.end()
        self.replot = False
        self.drawRect = False

    def draw( self ):
        """ Draw the figure when xwindows is ready for the update """
        self.replot = True
        self.update( )

    def blit(self, bbox=None):
        """ Blit the region in bbox """
        self.replot = bbox
        w, h = int(bbox.width()), int(bbox.height())
        l, t = bbox.ll().x().get(), bbox.ur().y().get()
        self.update(l, self.renderer.height-t, w, h)

    def print_figure(self, filename, dpi=None, facecolor='w', edgecolor='w',
                      orientation='portrait', **kwargs ):
        if dpi is None: dpi = matplotlib.rcParams['savefig.dpi']
        agg = self.switch_backends(FigureCanvasAgg)
        agg.print_figure(filename, dpi, facecolor, edgecolor, orientation,
                          **kwargs )
        self.figure.set_canvas(self)

    def print_dialog(self, printer=None):
        from PyQt4 import QtSvg
        if not printer:
            printer = QtGui.QPrinter()
        printer.setPageSize(QtGui.QPrinter.A4)
        dialog = QtGui.QPrintDialog(printer, self)
        dialog.setWindowTitle(QtCore.QCoreApplication.translate('MatPlot', 'Print Document'))
        if dialog.exec_() != QtGui.QDialog.Accepted:
            return
        painter = QtGui.QPainter(printer)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        f, name = tempfile.mkstemp('.svg')
        self.print_figure(name, dpi=300)
        renderer = QtSvg.QSvgRenderer(name)
        sBox = renderer.viewBox()
        tBox = painter.viewport()
        sRatio = sBox.width()/sBox.height()
        tRatio = tBox.width()/tBox.height()
        if sRatio > tRatio:
            painter.scale(1.0, tRatio/sRatio)
        else:
            painter.scale(sRatio/tRatio, 1.0)
        renderer.render(painter)
        #FIXME: without this the printer gets destroyed to early ...
        self.printer = printer

    def _get_key( self, event ):
        k = event.key()
        if k < 256:
            key = str(event.text())
        elif self.keyvald.has_key(k):
            key = self.keyvald[k]
        else:
            key = None
        return key


FigureManager = FigureManagerSV4

