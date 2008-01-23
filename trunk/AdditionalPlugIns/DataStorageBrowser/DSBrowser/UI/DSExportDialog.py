# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './DataStorageBrowser/DSBrowser/UI/DSExportDialog.ui'
#
# Created: Wed Jan 23 10:30:34 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DSExportDialog(object):
    def setupUi(self, DSExportDialog):
        DSExportDialog.setObjectName("DSExportDialog")
        DSExportDialog.resize(QtCore.QSize(QtCore.QRect(0,0,500,355).size()).expandedTo(DSExportDialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(DSExportDialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.fileLabel = QtGui.QLabel(DSExportDialog)
        self.fileLabel.setObjectName("fileLabel")
        self.hboxlayout.addWidget(self.fileLabel)

        self.fileNameInput = QtGui.QLineEdit(DSExportDialog)
        self.fileNameInput.setReadOnly(True)
        self.fileNameInput.setObjectName("fileNameInput")
        self.hboxlayout.addWidget(self.fileNameInput)

        self.fileNameButton = QtGui.QToolButton(DSExportDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileNameButton.sizePolicy().hasHeightForWidth())
        self.fileNameButton.setSizePolicy(sizePolicy)
        self.fileNameButton.setObjectName("fileNameButton")
        self.hboxlayout.addWidget(self.fileNameButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.sensorList = QtGui.QListWidget(DSExportDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensorList.sizePolicy().hasHeightForWidth())
        self.sensorList.setSizePolicy(sizePolicy)
        self.sensorList.setObjectName("sensorList")
        self.gridlayout.addWidget(self.sensorList,0,0,2,1)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        self.startLabel = QtGui.QLabel(DSExportDialog)
        self.startLabel.setObjectName("startLabel")
        self.gridlayout1.addWidget(self.startLabel,0,0,1,1)

        self.startInput = QtGui.QDateTimeEdit(DSExportDialog)
        self.startInput.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.startInput.setCalendarPopup(True)
        self.startInput.setObjectName("startInput")
        self.gridlayout1.addWidget(self.startInput,0,1,1,2)

        self.stopLabel = QtGui.QLabel(DSExportDialog)
        self.stopLabel.setObjectName("stopLabel")
        self.gridlayout1.addWidget(self.stopLabel,1,0,1,1)

        self.stopInput = QtGui.QDateTimeEdit(DSExportDialog)
        self.stopInput.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.stopInput.setCalendarPopup(True)
        self.stopInput.setObjectName("stopInput")
        self.gridlayout1.addWidget(self.stopInput,1,1,1,2)

        self.separatorLabel = QtGui.QLabel(DSExportDialog)
        self.separatorLabel.setObjectName("separatorLabel")
        self.gridlayout1.addWidget(self.separatorLabel,2,0,1,1)

        self.separatorInput = QtGui.QLineEdit(DSExportDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.separatorInput.sizePolicy().hasHeightForWidth())
        self.separatorInput.setSizePolicy(sizePolicy)
        self.separatorInput.setMinimumSize(QtCore.QSize(30,0))
        self.separatorInput.setMaximumSize(QtCore.QSize(30,16777215))
        self.separatorInput.setMaxLength(1)
        self.separatorInput.setObjectName("separatorInput")
        self.gridlayout1.addWidget(self.separatorInput,2,1,1,1)

        self.separatorHintLabel = QtGui.QLabel(DSExportDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.separatorHintLabel.sizePolicy().hasHeightForWidth())
        self.separatorHintLabel.setSizePolicy(sizePolicy)
        self.separatorHintLabel.setObjectName("separatorHintLabel")
        self.gridlayout1.addWidget(self.separatorHintLabel,2,2,1,1)

        self.openFileButton = QtGui.QCheckBox(DSExportDialog)
        self.openFileButton.setChecked(True)
        self.openFileButton.setObjectName("openFileButton")
        self.gridlayout1.addWidget(self.openFileButton,3,0,1,3)
        self.gridlayout.addLayout(self.gridlayout1,0,1,1,1)

        self.infoLabel = QtGui.QLabel(DSExportDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoLabel.sizePolicy().hasHeightForWidth())
        self.infoLabel.setSizePolicy(sizePolicy)
        self.infoLabel.setFrameShape(QtGui.QFrame.Box)
        self.infoLabel.setObjectName("infoLabel")
        self.gridlayout.addWidget(self.infoLabel,1,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.buttonBox = QtGui.QDialogButtonBox(DSExportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)
        self.separatorLabel.setBuddy(self.separatorInput)
        self.separatorHintLabel.setBuddy(self.separatorInput)

        self.retranslateUi(DSExportDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),DSExportDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),DSExportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DSExportDialog)

    def retranslateUi(self, DSExportDialog):
        DSExportDialog.setWindowTitle(QtGui.QApplication.translate("DSExportDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.fileLabel.setText(QtGui.QApplication.translate("DSExportDialog", "Filename/type:", None, QtGui.QApplication.UnicodeUTF8))
        self.fileNameButton.setText(QtGui.QApplication.translate("DSExportDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.startLabel.setText(QtGui.QApplication.translate("DSExportDialog", "Start time:", None, QtGui.QApplication.UnicodeUTF8))
        self.stopLabel.setText(QtGui.QApplication.translate("DSExportDialog", "End time:", None, QtGui.QApplication.UnicodeUTF8))
        self.separatorLabel.setText(QtGui.QApplication.translate("DSExportDialog", "Separator:", None, QtGui.QApplication.UnicodeUTF8))
        self.separatorInput.setText(QtGui.QApplication.translate("DSExportDialog", ";", None, QtGui.QApplication.UnicodeUTF8))
        self.separatorHintLabel.setText(QtGui.QApplication.translate("DSExportDialog", "(for CSV only)", None, QtGui.QApplication.UnicodeUTF8))
        self.openFileButton.setText(QtGui.QApplication.translate("DSExportDialog", "Open file after creation", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("DSExportDialog", "info", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DSExportDialog = QtGui.QDialog()
    ui = Ui_DSExportDialog()
    ui.setupUi(DSExportDialog)
    DSExportDialog.show()
    sys.exit(app.exec_())
