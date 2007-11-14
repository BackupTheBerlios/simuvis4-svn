# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SimuVis4/UI/LogView.ui'
#
# Created: Mon Feb 12 22:37:03 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_LogViewWidget(object):
    def setupUi(self, LogViewWidget):
        LogViewWidget.setObjectName("LogViewWidget")
        LogViewWidget.resize(QtCore.QSize(QtCore.QRect(0,0,686,409).size()).expandedTo(LogViewWidget.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(LogViewWidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.TextArea = QtGui.QTextEdit(LogViewWidget)
        self.TextArea.setReadOnly(True)
        self.TextArea.setObjectName("TextArea")
        self.vboxlayout.addWidget(self.TextArea)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(LogViewWidget)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.ThresholdSelector = QtGui.QComboBox(LogViewWidget)
        self.ThresholdSelector.setObjectName("ThresholdSelector")
        self.hboxlayout.addWidget(self.ThresholdSelector)

        spacerItem = QtGui.QSpacerItem(291,29,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.SaveButton = QtGui.QPushButton(LogViewWidget)
        self.SaveButton.setObjectName("SaveButton")
        self.hboxlayout.addWidget(self.SaveButton)

        self.ClearButton = QtGui.QPushButton(LogViewWidget)
        self.ClearButton.setObjectName("ClearButton")
        self.hboxlayout.addWidget(self.ClearButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(LogViewWidget)
        QtCore.QObject.connect(self.ClearButton,QtCore.SIGNAL("pressed()"),self.TextArea.clear)
        QtCore.QMetaObject.connectSlotsByName(LogViewWidget)

    def retranslateUi(self, LogViewWidget):
        LogViewWidget.setWindowTitle(QtGui.QApplication.translate("LogViewWidget", "Log Messages", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LogViewWidget", "Display Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveButton.setText(QtGui.QApplication.translate("LogViewWidget", "Save ...", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearButton.setText(QtGui.QApplication.translate("LogViewWidget", "Clear", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    LogViewWidget = QtGui.QWidget()
    ui = Ui_LogViewWidget()
    ui.setupUi(LogViewWidget)
    LogViewWidget.show()
    sys.exit(app.exec_())
