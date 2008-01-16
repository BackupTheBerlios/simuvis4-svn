# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SmileKit/SmileKit/UI/Mn2NcDialog.ui'
#
# Created: Fri Nov 30 12:39:50 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Mn2NcDialog(object):
    def setupUi(self, Mn2NcDialog):
        Mn2NcDialog.setObjectName("Mn2NcDialog")
        Mn2NcDialog.resize(QtCore.QSize(QtCore.QRect(0,0,367,609).size()).expandedTo(Mn2NcDialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Mn2NcDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.mnFileFrame = QtGui.QGroupBox(Mn2NcDialog)
        self.mnFileFrame.setObjectName("mnFileFrame")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.mnFileFrame)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.mnFileNameLabel = QtGui.QLabel(self.mnFileFrame)
        self.mnFileNameLabel.setObjectName("mnFileNameLabel")
        self.hboxlayout.addWidget(self.mnFileNameLabel)

        self.mnFileNameInput = QtGui.QLineEdit(self.mnFileFrame)
        self.mnFileNameInput.setObjectName("mnFileNameInput")
        self.hboxlayout.addWidget(self.mnFileNameInput)

        self.mnFileNameDialogButton = QtGui.QToolButton(self.mnFileFrame)
        self.mnFileNameDialogButton.setObjectName("mnFileNameDialogButton")
        self.hboxlayout.addWidget(self.mnFileNameDialogButton)
        self.vboxlayout1.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.mnFileLoadButton = QtGui.QPushButton(self.mnFileFrame)
        self.mnFileLoadButton.setObjectName("mnFileLoadButton")
        self.hboxlayout1.addWidget(self.mnFileLoadButton)

        self.helpButton = QtGui.QPushButton(self.mnFileFrame)
        self.helpButton.setObjectName("helpButton")
        self.hboxlayout1.addWidget(self.helpButton)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.vboxlayout1.addLayout(self.hboxlayout1)
        self.vboxlayout.addWidget(self.mnFileFrame)

        self.locationFrame = QtGui.QGroupBox(Mn2NcDialog)
        self.locationFrame.setObjectName("locationFrame")

        self.gridlayout = QtGui.QGridLayout(self.locationFrame)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.earthViewButton = QtGui.QPushButton(self.locationFrame)
        self.earthViewButton.setObjectName("earthViewButton")
        self.gridlayout.addWidget(self.earthViewButton,4,2,1,2)

        self.locHeightInput = QtGui.QSpinBox(self.locationFrame)
        self.locHeightInput.setAlignment(QtCore.Qt.AlignRight)
        self.locHeightInput.setMaximum(10000)
        self.locHeightInput.setMinimum(-100)
        self.locHeightInput.setObjectName("locHeightInput")
        self.gridlayout.addWidget(self.locHeightInput,3,1,1,1)

        self.locLatitudeInput = QtGui.QDoubleSpinBox(self.locationFrame)
        self.locLatitudeInput.setAlignment(QtCore.Qt.AlignRight)
        self.locLatitudeInput.setMaximum(90.0)
        self.locLatitudeInput.setMinimum(-90.0)
        self.locLatitudeInput.setObjectName("locLatitudeInput")
        self.gridlayout.addWidget(self.locLatitudeInput,2,1,1,1)

        self.locTimeZoneLabel = QtGui.QLabel(self.locationFrame)
        self.locTimeZoneLabel.setObjectName("locTimeZoneLabel")
        self.gridlayout.addWidget(self.locTimeZoneLabel,3,2,1,1)

        self.locHeightLabel = QtGui.QLabel(self.locationFrame)
        self.locHeightLabel.setObjectName("locHeightLabel")
        self.gridlayout.addWidget(self.locHeightLabel,3,0,1,1)

        self.locLatitudeLabel = QtGui.QLabel(self.locationFrame)
        self.locLatitudeLabel.setObjectName("locLatitudeLabel")
        self.gridlayout.addWidget(self.locLatitudeLabel,2,0,1,1)

        self.locTimeZoneInput = QtGui.QSpinBox(self.locationFrame)
        self.locTimeZoneInput.setAlignment(QtCore.Qt.AlignRight)
        self.locTimeZoneInput.setMaximum(23)
        self.locTimeZoneInput.setMinimum(-23)
        self.locTimeZoneInput.setSingleStep(1)
        self.locTimeZoneInput.setObjectName("locTimeZoneInput")
        self.gridlayout.addWidget(self.locTimeZoneInput,3,3,1,1)

        self.locNameLabel = QtGui.QLabel(self.locationFrame)
        self.locNameLabel.setObjectName("locNameLabel")
        self.gridlayout.addWidget(self.locNameLabel,0,0,1,1)

        self.locCommentLabel = QtGui.QLabel(self.locationFrame)
        self.locCommentLabel.setObjectName("locCommentLabel")
        self.gridlayout.addWidget(self.locCommentLabel,1,0,1,1)

        self.locCommentInput = QtGui.QLineEdit(self.locationFrame)
        self.locCommentInput.setObjectName("locCommentInput")
        self.gridlayout.addWidget(self.locCommentInput,1,1,1,3)

        self.locNameInput = QtGui.QLineEdit(self.locationFrame)
        self.locNameInput.setObjectName("locNameInput")
        self.gridlayout.addWidget(self.locNameInput,0,1,1,3)

        self.locLongitudeLabel = QtGui.QLabel(self.locationFrame)
        self.locLongitudeLabel.setObjectName("locLongitudeLabel")
        self.gridlayout.addWidget(self.locLongitudeLabel,2,2,1,1)

        self.locLongitudeInput = QtGui.QDoubleSpinBox(self.locationFrame)
        self.locLongitudeInput.setAlignment(QtCore.Qt.AlignRight)
        self.locLongitudeInput.setMaximum(180.0)
        self.locLongitudeInput.setMinimum(-180.0)
        self.locLongitudeInput.setObjectName("locLongitudeInput")
        self.gridlayout.addWidget(self.locLongitudeInput,2,3,1,1)
        self.vboxlayout.addWidget(self.locationFrame)

        self.statisticsFrame = QtGui.QGroupBox(Mn2NcDialog)
        self.statisticsFrame.setObjectName("statisticsFrame")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.statisticsFrame)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.statisticsButton = QtGui.QCheckBox(self.statisticsFrame)
        self.statisticsButton.setObjectName("statisticsButton")
        self.vboxlayout2.addWidget(self.statisticsButton)

        self.statisticsBrowser = QtGui.QTextBrowser(self.statisticsFrame)
        self.statisticsBrowser.setEnabled(False)
        self.statisticsBrowser.setMinimumSize(QtCore.QSize(0,100))
        self.statisticsBrowser.setObjectName("statisticsBrowser")
        self.vboxlayout2.addWidget(self.statisticsBrowser)
        self.vboxlayout.addWidget(self.statisticsFrame)

        self.ncFileFrame = QtGui.QGroupBox(Mn2NcDialog)
        self.ncFileFrame.setObjectName("ncFileFrame")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.ncFileFrame)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.ncFileNameLabel = QtGui.QLabel(self.ncFileFrame)
        self.ncFileNameLabel.setObjectName("ncFileNameLabel")
        self.hboxlayout2.addWidget(self.ncFileNameLabel)

        self.ncFileNameInput = QtGui.QLineEdit(self.ncFileFrame)
        self.ncFileNameInput.setObjectName("ncFileNameInput")
        self.hboxlayout2.addWidget(self.ncFileNameInput)

        self.ncFileNameDialogButton = QtGui.QToolButton(self.ncFileFrame)
        self.ncFileNameDialogButton.setObjectName("ncFileNameDialogButton")
        self.hboxlayout2.addWidget(self.ncFileNameDialogButton)
        self.vboxlayout3.addLayout(self.hboxlayout2)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.ncFileSaveButton = QtGui.QPushButton(self.ncFileFrame)
        self.ncFileSaveButton.setObjectName("ncFileSaveButton")
        self.hboxlayout3.addWidget(self.ncFileSaveButton)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem1)
        self.vboxlayout3.addLayout(self.hboxlayout3)
        self.vboxlayout.addWidget(self.ncFileFrame)

        self.retranslateUi(Mn2NcDialog)
        QtCore.QObject.connect(self.statisticsButton,QtCore.SIGNAL("toggled(bool)"),self.statisticsBrowser.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Mn2NcDialog)

    def retranslateUi(self, Mn2NcDialog):
        Mn2NcDialog.setWindowTitle(QtGui.QApplication.translate("Mn2NcDialog", "Meteonorm - netCDF Converter", None, QtGui.QApplication.UnicodeUTF8))
        self.mnFileFrame.setTitle(QtGui.QApplication.translate("Mn2NcDialog", "Meteonorm file", None, QtGui.QApplication.UnicodeUTF8))
        self.mnFileNameLabel.setText(QtGui.QApplication.translate("Mn2NcDialog", "File name:", None, QtGui.QApplication.UnicodeUTF8))
        self.mnFileNameDialogButton.setText(QtGui.QApplication.translate("Mn2NcDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.mnFileLoadButton.setText(QtGui.QApplication.translate("Mn2NcDialog", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.helpButton.setText(QtGui.QApplication.translate("Mn2NcDialog", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.locationFrame.setTitle(QtGui.QApplication.translate("Mn2NcDialog", "Location", None, QtGui.QApplication.UnicodeUTF8))
        self.earthViewButton.setText(QtGui.QApplication.translate("Mn2NcDialog", "Show 3D view", None, QtGui.QApplication.UnicodeUTF8))
        self.locHeightInput.setSuffix(QtGui.QApplication.translate("Mn2NcDialog", " m", None, QtGui.QApplication.UnicodeUTF8))
        self.locLatitudeInput.setSuffix(QtGui.QApplication.translate("Mn2NcDialog", " °", None, QtGui.QApplication.UnicodeUTF8))
        self.locTimeZoneLabel.setText(QtGui.QApplication.translate("Mn2NcDialog", "Time zone:", None, QtGui.QApplication.UnicodeUTF8))
        self.locHeightLabel.setText(QtGui.QApplication.translate("Mn2NcDialog", "Height:", None, QtGui.QApplication.UnicodeUTF8))
        self.locLatitudeLabel.setText(QtGui.QApplication.translate("Mn2NcDialog", "Latitude:", None, QtGui.QApplication.UnicodeUTF8))
        self.locTimeZoneInput.setSuffix(QtGui.QApplication.translate("Mn2NcDialog", " h", None, QtGui.QApplication.UnicodeUTF8))
        self.locNameLabel.setText(QtGui.QApplication.translate("Mn2NcDialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.locCommentLabel.setText(QtGui.QApplication.translate("Mn2NcDialog", "Comment:", None, QtGui.QApplication.UnicodeUTF8))
        self.locLongitudeLabel.setText(QtGui.QApplication.translate("Mn2NcDialog", "Longitude:", None, QtGui.QApplication.UnicodeUTF8))
        self.locLongitudeInput.setSuffix(QtGui.QApplication.translate("Mn2NcDialog", " °", None, QtGui.QApplication.UnicodeUTF8))
        self.statisticsFrame.setTitle(QtGui.QApplication.translate("Mn2NcDialog", "Statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.statisticsButton.setText(QtGui.QApplication.translate("Mn2NcDialog", "Enable statistical calculations", None, QtGui.QApplication.UnicodeUTF8))
        self.ncFileFrame.setTitle(QtGui.QApplication.translate("Mn2NcDialog", "netCDF file", None, QtGui.QApplication.UnicodeUTF8))
        self.ncFileNameLabel.setText(QtGui.QApplication.translate("Mn2NcDialog", "File name:", None, QtGui.QApplication.UnicodeUTF8))
        self.ncFileNameDialogButton.setText(QtGui.QApplication.translate("Mn2NcDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.ncFileSaveButton.setText(QtGui.QApplication.translate("Mn2NcDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Mn2NcDialog = QtGui.QWidget()
    ui = Ui_Mn2NcDialog()
    ui.setupUi(Mn2NcDialog)
    Mn2NcDialog.show()
    sys.exit(app.exec_())
