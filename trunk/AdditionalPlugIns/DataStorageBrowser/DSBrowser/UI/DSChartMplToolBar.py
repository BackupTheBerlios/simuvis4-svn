# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './DataStorageBrowser/DSBrowser/UI/DSChartMplToolBar.ui'
#
# Created: Wed Jan  9 14:57:06 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DSChartMplToolBar(object):
    def setupUi(self, DSChartMplToolBar):
        DSChartMplToolBar.setObjectName("DSChartMplToolBar")
        DSChartMplToolBar.resize(QtCore.QSize(QtCore.QRect(0,0,576,31).size()).expandedTo(DSChartMplToolBar.minimumSizeHint()))

        self.hboxlayout = QtGui.QHBoxLayout(DSChartMplToolBar)
        self.hboxlayout.setSpacing(2)
        self.hboxlayout.setMargin(1)
        self.hboxlayout.setObjectName("hboxlayout")

        self.GoStartButton = QtGui.QToolButton(DSChartMplToolBar)
        self.GoStartButton.setObjectName("GoStartButton")
        self.hboxlayout.addWidget(self.GoStartButton)

        self.GoBackButton = QtGui.QToolButton(DSChartMplToolBar)
        self.GoBackButton.setObjectName("GoBackButton")
        self.hboxlayout.addWidget(self.GoBackButton)

        self.GoForwardButton = QtGui.QToolButton(DSChartMplToolBar)
        self.GoForwardButton.setObjectName("GoForwardButton")
        self.hboxlayout.addWidget(self.GoForwardButton)

        self.GoEndButton = QtGui.QToolButton(DSChartMplToolBar)
        self.GoEndButton.setObjectName("GoEndButton")
        self.hboxlayout.addWidget(self.GoEndButton)

        self.StartLabel = QtGui.QLabel(DSChartMplToolBar)
        self.StartLabel.setObjectName("StartLabel")
        self.hboxlayout.addWidget(self.StartLabel)

        self.StartInput = QtGui.QDateTimeEdit(DSChartMplToolBar)
        self.StartInput.setCalendarPopup(True)
        self.StartInput.setObjectName("StartInput")
        self.hboxlayout.addWidget(self.StartInput)

        self.LengthLabel = QtGui.QLabel(DSChartMplToolBar)
        self.LengthLabel.setObjectName("LengthLabel")
        self.hboxlayout.addWidget(self.LengthLabel)

        self.LengthInput = QtGui.QSpinBox(DSChartMplToolBar)
        self.LengthInput.setMinimum(1)
        self.LengthInput.setMaximum(365)
        self.LengthInput.setObjectName("LengthInput")
        self.hboxlayout.addWidget(self.LengthInput)

        self.LengthUnitInput = QtGui.QComboBox(DSChartMplToolBar)
        self.LengthUnitInput.setObjectName("LengthUnitInput")
        self.hboxlayout.addWidget(self.LengthUnitInput)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.AnimationButton = QtGui.QToolButton(DSChartMplToolBar)
        self.AnimationButton.setCheckable(True)
        self.AnimationButton.setArrowType(QtCore.Qt.NoArrow)
        self.AnimationButton.setObjectName("AnimationButton")
        self.hboxlayout.addWidget(self.AnimationButton)

        self.AnimationDelayInput = QtGui.QSpinBox(DSChartMplToolBar)
        self.AnimationDelayInput.setMinimum(1)
        self.AnimationDelayInput.setMaximum(60)
        self.AnimationDelayInput.setProperty("value",QtCore.QVariant(5))
        self.AnimationDelayInput.setObjectName("AnimationDelayInput")
        self.hboxlayout.addWidget(self.AnimationDelayInput)

        self.retranslateUi(DSChartMplToolBar)
        QtCore.QMetaObject.connectSlotsByName(DSChartMplToolBar)
        DSChartMplToolBar.setTabOrder(self.GoStartButton,self.GoBackButton)
        DSChartMplToolBar.setTabOrder(self.GoBackButton,self.GoForwardButton)
        DSChartMplToolBar.setTabOrder(self.GoForwardButton,self.GoEndButton)
        DSChartMplToolBar.setTabOrder(self.GoEndButton,self.StartInput)
        DSChartMplToolBar.setTabOrder(self.StartInput,self.LengthInput)
        DSChartMplToolBar.setTabOrder(self.LengthInput,self.LengthUnitInput)
        DSChartMplToolBar.setTabOrder(self.LengthUnitInput,self.AnimationButton)
        DSChartMplToolBar.setTabOrder(self.AnimationButton,self.AnimationDelayInput)

    def retranslateUi(self, DSChartMplToolBar):
        DSChartMplToolBar.setWindowTitle(QtGui.QApplication.translate("DSChartMplToolBar", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.GoStartButton.setToolTip(QtGui.QApplication.translate("DSChartMplToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Got to start of the time interval</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GoStartButton.setText(QtGui.QApplication.translate("DSChartMplToolBar", "|<", None, QtGui.QApplication.UnicodeUTF8))
        self.GoBackButton.setToolTip(QtGui.QApplication.translate("DSChartMplToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Go back one step</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GoBackButton.setText(QtGui.QApplication.translate("DSChartMplToolBar", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.GoForwardButton.setToolTip(QtGui.QApplication.translate("DSChartMplToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Go forward one step</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GoForwardButton.setText(QtGui.QApplication.translate("DSChartMplToolBar", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.GoEndButton.setToolTip(QtGui.QApplication.translate("DSChartMplToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Got to the end of the time interval</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GoEndButton.setText(QtGui.QApplication.translate("DSChartMplToolBar", ">|", None, QtGui.QApplication.UnicodeUTF8))
        self.StartLabel.setText(QtGui.QApplication.translate("DSChartMplToolBar", "Start:", None, QtGui.QApplication.UnicodeUTF8))
        self.StartInput.setToolTip(QtGui.QApplication.translate("DSChartMplToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select start date and time</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthLabel.setText(QtGui.QApplication.translate("DSChartMplToolBar", "Length:", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthInput.setToolTip(QtGui.QApplication.translate("DSChartMplToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select length of one step (visible time range)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.setToolTip(QtGui.QApplication.translate("DSChartMplToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select unit of step length</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSChartMplToolBar", "Minutes", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSChartMplToolBar", "Hours", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSChartMplToolBar", "Days", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSChartMplToolBar", "Weeks", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSChartMplToolBar", "Months", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthUnitInput.addItem(QtGui.QApplication.translate("DSChartMplToolBar", "Years", None, QtGui.QApplication.UnicodeUTF8))
        self.AnimationButton.setToolTip(QtGui.QApplication.translate("DSChartMplToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Start animation</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.AnimationButton.setText(QtGui.QApplication.translate("DSChartMplToolBar", "»", None, QtGui.QApplication.UnicodeUTF8))
        self.AnimationDelayInput.setToolTip(QtGui.QApplication.translate("DSChartMplToolBar", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Verdana\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Animation delay between steps</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.AnimationDelayInput.setSuffix(QtGui.QApplication.translate("DSChartMplToolBar", " s", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DSChartMplToolBar = QtGui.QWidget()
    ui = Ui_DSChartMplToolBar()
    ui.setupUi(DSChartMplToolBar)
    DSChartMplToolBar.show()
    sys.exit(app.exec_())
