# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from PyQt4.QtGui import QWidget, QVBoxLayout, QIcon, QPixmap, QAction, QMessageBox, QFileDialog, QDialog
from PyQt4.QtCore import QCoreApplication, SIGNAL
import Globals, os

printMsg = QCoreApplication.translate('SubWindow',
"""<p>This window can't be printed, but you
may save a screenshot instead.</p>

<p>A <b>widget screenshot</b> will work in most cases.</p>

<p>For some windows (especially vtk) you may need a
<b>window screenshot</b>. Make sure the window is
not covered by another dialog or window!</p>
""")

class SubWindow(QWidget):

    """base class for subwindows of the mdi workspace"""

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setMargin(0)
        self.mainLayout.setSpacing(6)
        icon = os.path.join(Globals.config['main:system_picture_path'], 'subwin.xpm')
        self.setWindowIcon(QIcon(QPixmap(icon)))
        self.setWindowTitle(QCoreApplication.translate('SubWindow', 'Unnamed Subwindow'))
        self.toggleVisibleAction = QAction(self)
        self.toggleVisibleAction.setCheckable(True)
        self.connect(self.toggleVisibleAction, SIGNAL("toggled(bool)"), self.setVisible)
        # FIXME: make close(), hide(), show*() change the actions state!


    def printWindow(self, p):
        save = QMessageBox.question(self,
            QCoreApplication.translate('SubWindow', 'Save Screenshot?'),
            printMsg,
            QCoreApplication.translate('SubWindow', 'Widget'),
            QCoreApplication.translate('SubWindow', 'Window'),
            QCoreApplication.translate('SubWindow', 'No'),
        )
        if save == 0:
            self.saveWindow()
        elif save == 1:
            self.saveWindow(window=True)


    def saveWindow(self, fileName=None, fileType=None, window=False):
        self.repaint() # make sure we are uptodate
        if window:
            pixmap = QPixmap.grabWindow(self.winId())
        else:
            pixmap = QPixmap.grabWidget(self)
        if not fileName:
            fileTypes = {unicode(QCoreApplication.translate('SubWindow', 'PNG - compressed image')):('png',),
                unicode(QCoreApplication.translate('SubWindow', 'JPEG - picture')):('jpg', 'jpeg'),
                unicode(QCoreApplication.translate('SubWindow', 'BMP - uncompressed bitmap')):('bmp',)}
            filters = ';;'.join(['%s (%s)' % (k, ' '.join(['*.'+e for e in v])) for k, v in fileTypes.items()])
            dlg = QFileDialog(self,
                QCoreApplication.translate('SubWindow', 'Select name of file to save'),
                Globals.defaultFolder or '', filters)
            dlg.setFileMode(QFileDialog.AnyFile)
            dlg.setAcceptMode(QFileDialog.AcceptSave)
            if dlg.exec_() != QDialog.Accepted:
                return
            tmp = unicode(dlg.selectedFilter())
            fileType = tmp[:tmp.find('(')-1]
            dlg.setDefaultSuffix(fileTypes[fileType][0])
            files = dlg.selectedFiles()
            if not files:
                return
            fileName = unicode(files[0])
            Globals.defaultFolder, tmp = os.path.split(fileName)
        try:
            pixmap.save(unicode(fileName))
        except:
            QMessageBox.critical(self,
                QCoreApplication.translate('SubWindow', 'Could not save file!'),
                QCoreApplication.translate('SubWindow', 'Writing failed! Make sure you have write permissions!'))
