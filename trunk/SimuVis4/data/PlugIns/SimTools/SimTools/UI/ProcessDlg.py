# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './data/PlugIns/SimTools/SimTools/UI/ProcessDlg.ui'
#
# Created: Wed May  9 13:48:31 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProcessDlg(object):
    def setupUi(self, ProcessDlg):
        ProcessDlg.setObjectName("ProcessDlg")
        ProcessDlg.resize(QtCore.QSize(QtCore.QRect(0,0,434,253).size()).expandedTo(ProcessDlg.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ProcessDlg)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.folderLabel = QtGui.QLabel(ProcessDlg)
        self.folderLabel.setObjectName("folderLabel")
        self.gridlayout.addWidget(self.folderLabel,1,0,1,1)

        self.commandLabel = QtGui.QLabel(ProcessDlg)
        self.commandLabel.setObjectName("commandLabel")
        self.gridlayout.addWidget(self.commandLabel,0,0,1,1)

        self.commandInput = QtGui.QLineEdit(ProcessDlg)
        self.commandInput.setObjectName("commandInput")
        self.gridlayout.addWidget(self.commandInput,0,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.folderInput = QtGui.QLineEdit(ProcessDlg)
        self.folderInput.setEnabled(False)
        self.folderInput.setObjectName("folderInput")
        self.hboxlayout.addWidget(self.folderInput)

        self.folderButton = QtGui.QToolButton(ProcessDlg)
        self.folderButton.setEnabled(False)
        self.folderButton.setObjectName("folderButton")
        self.hboxlayout.addWidget(self.folderButton)

        self.folderAutoButton = QtGui.QCheckBox(ProcessDlg)
        self.folderAutoButton.setChecked(True)
        self.folderAutoButton.setObjectName("folderAutoButton")
        self.hboxlayout.addWidget(self.folderAutoButton)
        self.gridlayout.addLayout(self.hboxlayout,1,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.showOutputButton = QtGui.QCheckBox(ProcessDlg)
        self.showOutputButton.setChecked(True)
        self.showOutputButton.setObjectName("showOutputButton")
        self.hboxlayout1.addWidget(self.showOutputButton)

        self.autoCloseButton = QtGui.QCheckBox(ProcessDlg)
        self.autoCloseButton.setObjectName("autoCloseButton")
        self.hboxlayout1.addWidget(self.autoCloseButton)

        spacerItem = QtGui.QSpacerItem(147,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.advancedSettingsButton = QtGui.QPushButton(ProcessDlg)
        self.advancedSettingsButton.setEnabled(False)
        self.advancedSettingsButton.setObjectName("advancedSettingsButton")
        self.hboxlayout1.addWidget(self.advancedSettingsButton)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.outputView = QtGui.QTextEdit(ProcessDlg)
        self.outputView.setObjectName("outputView")
        self.vboxlayout.addWidget(self.outputView)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.statusLabel = QtGui.QLabel(ProcessDlg)
        self.statusLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.statusLabel.setObjectName("statusLabel")
        self.hboxlayout2.addWidget(self.statusLabel)

        spacerItem1 = QtGui.QSpacerItem(201,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)

        self.startButton = QtGui.QPushButton(ProcessDlg)
        self.startButton.setEnabled(False)
        self.startButton.setAutoDefault(True)
        self.startButton.setDefault(True)
        self.startButton.setObjectName("startButton")
        self.hboxlayout2.addWidget(self.startButton)

        self.closeButton = QtGui.QPushButton(ProcessDlg)
        self.closeButton.setObjectName("closeButton")
        self.hboxlayout2.addWidget(self.closeButton)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(ProcessDlg)
        QtCore.QObject.connect(self.folderAutoButton,QtCore.SIGNAL("toggled(bool)"),self.folderButton.setDisabled)
        QtCore.QObject.connect(self.folderAutoButton,QtCore.SIGNAL("toggled(bool)"),self.folderInput.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(ProcessDlg)

    def retranslateUi(self, ProcessDlg):
        ProcessDlg.setWindowTitle(QtGui.QApplication.translate("ProcessDlg", "Process", None, QtGui.QApplication.UnicodeUTF8))
        self.folderLabel.setText(QtGui.QApplication.translate("ProcessDlg", "Folder: ", None, QtGui.QApplication.UnicodeUTF8))
        self.commandLabel.setText(QtGui.QApplication.translate("ProcessDlg", "Command: ", None, QtGui.QApplication.UnicodeUTF8))
        self.folderButton.setText(QtGui.QApplication.translate("ProcessDlg", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.folderAutoButton.setText(QtGui.QApplication.translate("ProcessDlg", "Auto", None, QtGui.QApplication.UnicodeUTF8))
        self.showOutputButton.setText(QtGui.QApplication.translate("ProcessDlg", "Show output", None, QtGui.QApplication.UnicodeUTF8))
        self.autoCloseButton.setText(QtGui.QApplication.translate("ProcessDlg", "Auto-close", None, QtGui.QApplication.UnicodeUTF8))
        self.advancedSettingsButton.setText(QtGui.QApplication.translate("ProcessDlg", "Advanced", None, QtGui.QApplication.UnicodeUTF8))
        self.statusLabel.setText(QtGui.QApplication.translate("ProcessDlg", "Status: waiting", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("ProcessDlg", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("ProcessDlg", "Close", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ProcessDlg = QtGui.QWidget()
    ui = Ui_ProcessDlg()
    ui.setupUi(ProcessDlg)
    ProcessDlg.show()
    sys.exit(app.exec_())
