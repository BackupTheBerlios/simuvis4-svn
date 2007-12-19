# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './DataStorageBrowser/DSBrowser/UI/DSGraphToolBar.ui'
#
# Created: Wed Dec 19 11:26:13 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DSGraphToolBar(object):
    def setupUi(self, DSGraphToolBar):
        DSGraphToolBar.setObjectName("DSGraphToolBar")
        DSGraphToolBar.resize(QtCore.QSize(QtCore.QRect(0,0,649,33).size()).expandedTo(DSGraphToolBar.minimumSizeHint()))

        self.hboxlayout = QtGui.QHBoxLayout(DSGraphToolBar)
        self.hboxlayout.setContentsMargins(-1,3,3,3)
        self.hboxlayout.setObjectName("hboxlayout")

        self.GoStartButton = QtGui.QToolButton(DSGraphToolBar)
        self.GoStartButton.setObjectName("GoStartButton")
        self.hboxlayout.addWidget(self.GoStartButton)

        self.GoBackButton = QtGui.QToolButton(DSGraphToolBar)
        self.GoBackButton.setObjectName("GoBackButton")
        self.hboxlayout.addWidget(self.GoBackButton)

        self.GoForwardButton = QtGui.QToolButton(DSGraphToolBar)
        self.GoForwardButton.setObjectName("GoForwardButton")
        self.hboxlayout.addWidget(self.GoForwardButton)

        self.GoEndButton = QtGui.QToolButton(DSGraphToolBar)
        self.GoEndButton.setObjectName("GoEndButton")
        self.hboxlayout.addWidget(self.GoEndButton)

        self.StartLabel = QtGui.QLabel(DSGraphToolBar)
        self.StartLabel.setObjectName("StartLabel")
        self.hboxlayout.addWidget(self.StartLabel)

        self.StartInput = QtGui.QDateTimeEdit(DSGraphToolBar)
        self.StartInput.setCalendarPopup(True)
        self.StartInput.setObjectName("StartInput")
        self.hboxlayout.addWidget(self.StartInput)

        self.LengthLabel = QtGui.QLabel(DSGraphToolBar)
        self.LengthLabel.setObjectName("LengthLabel")
        self.hboxlayout.addWidget(self.LengthLabel)

        self.LengthInput = QtGui.QSpinBox(DSGraphToolBar)
        self.LengthInput.setMinimum(1)
        self.LengthInput.setMaximum(365)
        self.LengthInput.setObjectName("LengthInput")
        self.hboxlayout.addWidget(self.LengthInput)

        self.LengthUnitInput = QtGui.QComboBox(DSGraphToolBar)
        self.LengthUnitInput.setObjectName("LengthUnitInput")
        self.hboxlayout.addWidget(self.LengthUnitInput)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.AnimationButton = QtGui.QToolButton(DSGraphToolBar)
        self.AnimationButton.setCheckable(True)
        self.AnimationButton.setObjectName("AnimationButton")
        self.hboxlayout.addWidget(self.AnimationButton)

        self.AnimationDelayInput = QtGui.QSpinBox(DSGraphToolBar)
        self.AnimationDelayInput.setMinimum(1)
        self.AnimationDelayInput.setMaximum(60)
        self.AnimationDelayInput.setProperty("value",QtCore.QVariant(5))
        self.AnimationDelayInput.setObjectName("AnimationDelayInput")
        self.hboxlayout.addWidget(self.AnimationDelayInput)

        self.retranslateUi(DSGraphToolBar)
        QtCore.QMetaObject.connectSlotsByName(DSGraphToolBar)
        DSGraphToolBar.setTabOrder(self.GoStartButton,self.GoBackButton)
        DSGraphToolBar.setTabOrder(self.GoBackButton,self.GoForwardButton)
        DSGraphToolBar.setTabOrder(self.GoForwardButton,self.GoEndButton)
        DSGraphToolBar.setTabOrder(self.GoEndButton,self.StartInput)
        DSGraphToolBar.setTabOrder(self.StartInput,self.LengthInput)
        DSGraphToolBar.setTabOrder(self.LengthInput,self.LengthUnitInput)
        DSGraphToolBar.setTabOrder(self.LengthUnitInput,self.AnimationButton)
        DSGraphToolBar.setTabOrder(self.AnimationButton,self.AnimationDelayInput)

    def retranslateUi(self, DSGraphToolBar):
        DSGraphToolBar.setWindowTitle(QtGui.QApplication.translate("DSGraphToolBar", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.GoStartButton.setToolTip(QtGui.QApplication.translate("DSGraphToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Got to start of the time interval</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GoStartButton.setText(QtGui.QApplication.translate("DSGraphToolBar", "|<", None, QtGui.QApplication.UnicodeUTF8))
        self.GoBackButton.setToolTip(QtGui.QApplication.translate("DSGraphToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Go back one step</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GoBackButton.setText(QtGui.QApplication.translate("DSGraphToolBar", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.GoForwardButton.setToolTip(QtGui.QApplication.translate("DSGraphToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Go forward one step</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GoForwardButton.setText(QtGui.QApplication.translate("DSGraphToolBar", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.GoEndButton.setToolTip(QtGui.QApplication.translate("DSGraphToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Got to the end of the time interval</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GoEndButton.setText(QtGui.QApplication.translate("DSGraphToolBar", ">|", None, QtGui.QApplication.UnicodeUTF8))
        self.StartLabel.setText(QtGui.QApplication.translate("DSGraphToolBar", "Start:", None, QtGui.QApplication.UnicodeUTF8))
        self.StartInput.setToolTip(QtGui.QApplication.translate("DSGraphToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select start date and time</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthLabel.setText(QtGui.QApplication.translate("DSGraphToolBar", "Length:", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthInput.setToolTip(QtGui.QApplication.translate("DSGraphToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select length of one step (visible time range)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.setToolTip(QtGui.QApplication.translate("DSGraphToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select unit of step length</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSGraphToolBar", "Hours", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSGraphToolBar", "Days", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSGraphToolBar", "Weeks", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSGraphToolBar", "Months", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSGraphToolBar", "Years", None, QtGui.QApplication.UnicodeUTF8))
        self.AnimationButton.setToolTip(QtGui.QApplication.translate("DSGraphToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Start animation</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.AnimationButton.setText(QtGui.QApplication.translate("DSGraphToolBar", "»", None, QtGui.QApplication.UnicodeUTF8))
        self.AnimationDelayInput.setToolTip(QtGui.QApplication.translate("DSGraphToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Animation delay between steps</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.AnimationDelayInput.setSuffix(QtGui.QApplication.translate("DSGraphToolBar", " s", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DSGraphToolBar = QtGui.QWidget()
    ui = Ui_DSGraphToolBar()
    ui.setupUi(DSGraphToolBar)
    DSGraphToolBar.show()
    sys.exit(app.exec_())
