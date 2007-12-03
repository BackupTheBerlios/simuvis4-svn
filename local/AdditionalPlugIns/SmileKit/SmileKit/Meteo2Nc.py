# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4
from PyQt4.QtGui import QWidget, QVBoxLayout, QProgressDialog, QFileDialog, QMessageBox, QCheckBox
from PyQt4.QtCore import Qt, QCoreApplication, SIGNAL, QTimer

from UI.Mn2NcDialog import Ui_Mn2NcDialog
import SimuVis4.Globals as glb

try:
    from MeteonormFile import readMnFile, writeNcFile, makeStatistics, version, mnHelpText
except ImportError:
    SimuVis4.Globals.logger.error(QCoreApplication.translate('SmileKit',
        'SmileKit: support for netCDF3 not found, Meteonorm file conversion will not work!'))

import os, time


def makeFileName(s):
    return s.strip().replace(' ', '_').replace('!', '_')


class Meteo2NcWidget(QWidget, Ui_Mn2NcDialog):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.locationFrame.setDisabled(1)
        self.statisticsFrame.setDisabled(1)
        self.ncFileFrame.setDisabled(1)
        self.connect(self.mnFileLoadButton, SIGNAL("pressed()"), self.loadFile)
        self.connect(self.helpButton, SIGNAL("pressed()"), self.showHelp)
        self.connect(self.mnFileNameDialogButton, SIGNAL("pressed()"), self.mnFileNameDialog)
        self.connect(self.ncFileSaveButton, SIGNAL("pressed()"), self.saveFile)
        self.connect(self.ncFileNameDialogButton, SIGNAL("pressed()"), self.ncFileNameDialog)
        self.connect(self.earthViewButton, SIGNAL("pressed()"), self.showEarthView)
        self.connect(self.statisticsButton, SIGNAL("toggled(bool)"), self.showStatistics)
        self.data = None

    def mnFileNameDialog(self):
        fileName = unicode(QFileDialog.getOpenFileName(self, QCoreApplication.translate('SmileKit',
            "Select Meteonorm file to open"), glb.defaultFolder))
        if fileName:
            glb.defaultFolder, tmp = os.path.split(fileName)
            self.mnFileNameInput.setText(fileName)

    def showHelp(self):
        QMessageBox.information(glb.mainWin,
            QCoreApplication.translate('SmileKit', 'HowTo generate a Meteonorm-5 file'),
            mnHelpText)

    def loadFile(self):
        mnFileName = unicode(self.mnFileNameInput.text())
        if not mnFileName:
            QMessageBox.warning(glb.mainWin,
                QCoreApplication.translate('SmileKit', 'No filename specified'),
                QCoreApplication.translate('SmileKit', 'Please enter a filename in the input box!'))
            return
        progressDlg = QProgressDialog(glb.mainWin)
        progressDlg.setRange(0, 100)
        progressDlg.setLabelText('Reading File...')
        progressDlg.show()
        a = glb.application
        def progFunc(p):
            progressDlg.setValue(p)
            if a.hasPendingEvents():
                a.processEvents()
        r = readMnFile(mnFileName, progress=progFunc)
        self.data = r
        progressDlg.close()
        self.locationFrame.setEnabled(1)
        self.statisticsFrame.setEnabled(1)
        self.ncFileFrame.setEnabled(1)
        self.statisticsButton.setCheckState(Qt.Unchecked)
        self.locNameInput.setText(r['name'])
        c = unicode(QCoreApplication.translate('SmileKit', "created %s from %s by Meteo2Nc.py (v%d)"))
        self.locCommentInput.setText(c % (time.ctime(), mnFileName, version))
        self.locLatitudeInput.setValue(r['latitude'])
        self.locLongitudeInput.setValue(r['longitude'])
        self.locHeightInput.setValue(r['height'])
        self.locTimeZoneInput.setValue(r['timezone'])
        path, tmp = os.path.split(mnFileName)
        ncFileName = os.path.join(path, makeFileName(r['name'])+'_weather.nc')
        self.ncFileNameInput.setText(ncFileName)

    def showStatistics(self, b):
        if b:
            txt = makeStatistics(self.data)
            self.statisticsBrowser.setText('<pre>%s\n</pre>' % txt)
        else:
            self.statisticsBrowser.clear()

    def ncFileNameDialog(self):
        fileName = unicode(QFileDialog.getSaveFileName(self, QCoreApplication.translate('SmileKit',
            "Select netCDF file to save"), self.ncFileNameInput.text()))
        if fileName:
            glb.defaultFolder, tmp = os.path.split(fileName)
            self.ncFileNameInput.setText(fileName)

    def saveFile(self):
        ncFileName = unicode(self.ncFileNameInput.text())
        if not ncFileName:
            QMessageBox.warning(glb.mainWin,
                QCoreApplication.translate('SmileKit', 'No filename specified'),
                QCoreApplication.translate('SmileKit', 'Please enter a filename in the input box!'))
            return
        writeNcFile(self.data, ncFileName)
        QMessageBox.information(glb.mainWin,
                QCoreApplication.translate('SmileKit', 'netCDF file saved!'),
                QCoreApplication.translate('SmileKit', 'The netCDF file was successfully saved!'))

    def showEarthView(self):
        vtkPI = glb.mainWin.plugInManager.getPlugIn('VtkWindow')
        if not vtkPI:
            return
        earthViewWindow = vtkPI.winManager.newWindow('Weather data location view')
        ren = vtkPI.vtk.vtkRenderer()
        earthViewWindow.vtkWidget.GetRenderWindow().AddRenderer(ren)
        earth = vtkPI.Objects.Earth()
        earth.showGrid()
        earth.showTexture()
        loc = earth.showPosition(self.locLatitudeInput.value(), -self.locLongitudeInput.value(),
            unicode(self.locNameInput.text()))
        tz = earth.showPosition(self.locLatitudeInput.value(), -15.0*self.locTimeZoneInput.value(), "Timezone")
        earth.addToRenderer(ren)
        ren.AddActor(loc)
        ren.AddActor(tz)
        earthViewWindow.resize(400, 400)


class Meteo2NcWindow(SimuVis4.SubWin.SubWindow):

    def __init__(self, parent):
        SimuVis4.SubWin.SubWindow.__init__(self, parent)
        self.setWindowTitle(QCoreApplication.translate('SmileKit', 'Meteonorm weather import'))
        self.meteo2NcWidget = Meteo2NcWidget(self)
        self.setWidget(self.meteo2NcWidget)

