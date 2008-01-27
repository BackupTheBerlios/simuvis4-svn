# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './data/PlugIns/SimTools/SimTools/UI/TimeSignalWidget.ui'
#
# Created: Sat Feb 17 19:33:34 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_TimeSignalWidget(object):
    def setupUi(self, TimeSignalWidget):
        TimeSignalWidget.setObjectName("TimeSignalWidget")
        TimeSignalWidget.resize(QtCore.QSize(QtCore.QRect(0,0,301,378).size()).expandedTo(TimeSignalWidget.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(TimeSignalWidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.runStopButton = QtGui.QPushButton(TimeSignalWidget)

        font = QtGui.QFont(self.runStopButton.font())
        font.setWeight(75)
        font.setBold(True)
        self.runStopButton.setFont(font)
        self.runStopButton.setCheckable(True)
        self.runStopButton.setAutoDefault(True)
        self.runStopButton.setDefault(True)
        self.runStopButton.setObjectName("runStopButton")
        self.hboxlayout.addWidget(self.runStopButton)

        self.stepButton = QtGui.QPushButton(TimeSignalWidget)
        self.stepButton.setFlat(False)
        self.stepButton.setObjectName("stepButton")
        self.hboxlayout.addWidget(self.stepButton)

        self.resetButton = QtGui.QPushButton(TimeSignalWidget)
        self.resetButton.setObjectName("resetButton")
        self.hboxlayout.addWidget(self.resetButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.speedFrame = QtGui.QGroupBox(TimeSignalWidget)
        self.speedFrame.setObjectName("speedFrame")

        self.gridlayout = QtGui.QGridLayout(self.speedFrame)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.frequencyInput = QtGui.QDoubleSpinBox(self.speedFrame)
        self.frequencyInput.setDecimals(6)
        self.frequencyInput.setMaximum(9999.99)
        self.frequencyInput.setMinimum(0.001)
        self.frequencyInput.setProperty("value",QtCore.QVariant(10.0))
        self.frequencyInput.setObjectName("frequencyInput")
        self.gridlayout.addWidget(self.frequencyInput,1,1,1,1)

        self.stepSizeInput = QtGui.QDoubleSpinBox(self.speedFrame)
        self.stepSizeInput.setDecimals(6)
        self.stepSizeInput.setMaximum(999.99)
        self.stepSizeInput.setMinimum(0.001)
        self.stepSizeInput.setProperty("value",QtCore.QVariant(0.1))
        self.stepSizeInput.setObjectName("stepSizeInput")
        self.gridlayout.addWidget(self.stepSizeInput,0,1,1,1)

        self.frequencyLabel = QtGui.QLabel(self.speedFrame)
        self.frequencyLabel.setObjectName("frequencyLabel")
        self.gridlayout.addWidget(self.frequencyLabel,1,0,1,1)

        self.stepSizeLabel = QtGui.QLabel(self.speedFrame)
        self.stepSizeLabel.setObjectName("stepSizeLabel")
        self.gridlayout.addWidget(self.stepSizeLabel,0,0,1,1)
        self.vboxlayout.addWidget(self.speedFrame)

        self.signalFrame = QtGui.QGroupBox(TimeSignalWidget)
        self.signalFrame.setObjectName("signalFrame")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.signalFrame)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.startValueLabel = QtGui.QLabel(self.signalFrame)
        self.startValueLabel.setObjectName("startValueLabel")
        self.hboxlayout1.addWidget(self.startValueLabel)

        self.startValueInput = QtGui.QDoubleSpinBox(self.signalFrame)
        self.startValueInput.setDecimals(6)
        self.startValueInput.setMaximum(100000000.0)
        self.startValueInput.setMinimum(0.0)
        self.startValueInput.setObjectName("startValueInput")
        self.hboxlayout1.addWidget(self.startValueInput)
        self.vboxlayout1.addLayout(self.hboxlayout1)

        self.compValueButton = QtGui.QRadioButton(self.signalFrame)
        self.compValueButton.setChecked(True)
        self.compValueButton.setObjectName("compValueButton")
        self.vboxlayout1.addWidget(self.compValueButton)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.stepLabel = QtGui.QLabel(self.signalFrame)
        self.stepLabel.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stepLabel.sizePolicy().hasHeightForWidth())
        self.stepLabel.setSizePolicy(sizePolicy)
        self.stepLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.stepLabel.setObjectName("stepLabel")
        self.hboxlayout2.addWidget(self.stepLabel)

        self.compValueStepInput = QtGui.QDoubleSpinBox(self.signalFrame)
        self.compValueStepInput.setEnabled(True)
        self.compValueStepInput.setDecimals(6)
        self.compValueStepInput.setMaximum(100000000.0)
        self.compValueStepInput.setMinimum(-100000000.0)
        self.compValueStepInput.setProperty("value",QtCore.QVariant(1.0))
        self.compValueStepInput.setObjectName("compValueStepInput")
        self.hboxlayout2.addWidget(self.compValueStepInput)

        self.signalRatioLabel = QtGui.QLabel(self.signalFrame)
        self.signalRatioLabel.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.signalRatioLabel.sizePolicy().hasHeightForWidth())
        self.signalRatioLabel.setSizePolicy(sizePolicy)
        self.signalRatioLabel.setObjectName("signalRatioLabel")
        self.hboxlayout2.addWidget(self.signalRatioLabel)
        self.vboxlayout1.addLayout(self.hboxlayout2)

        self.realTimeButton = QtGui.QRadioButton(self.signalFrame)
        self.realTimeButton.setChecked(False)
        self.realTimeButton.setObjectName("realTimeButton")
        self.vboxlayout1.addWidget(self.realTimeButton)
        self.vboxlayout.addWidget(self.signalFrame)

        self.signalFrame1 = QtGui.QGroupBox(TimeSignalWidget)
        self.signalFrame1.setObjectName("signalFrame1")

        self.hboxlayout3 = QtGui.QHBoxLayout(self.signalFrame1)
        self.hboxlayout3.setMargin(9)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.signalLabel = QtGui.QLabel(self.signalFrame1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.signalLabel.sizePolicy().hasHeightForWidth())
        self.signalLabel.setSizePolicy(sizePolicy)
        self.signalLabel.setObjectName("signalLabel")
        self.hboxlayout3.addWidget(self.signalLabel)

        self.signalShowButton = QtGui.QCheckBox(self.signalFrame1)
        self.signalShowButton.setChecked(True)
        self.signalShowButton.setObjectName("signalShowButton")
        self.hboxlayout3.addWidget(self.signalShowButton)
        self.vboxlayout.addWidget(self.signalFrame1)

        self.retranslateUi(TimeSignalWidget)
        QtCore.QObject.connect(self.compValueButton,QtCore.SIGNAL("toggled(bool)"),self.stepLabel.setEnabled)
        QtCore.QObject.connect(self.compValueButton,QtCore.SIGNAL("toggled(bool)"),self.compValueStepInput.setEnabled)
        QtCore.QObject.connect(self.compValueButton,QtCore.SIGNAL("toggled(bool)"),self.signalRatioLabel.setEnabled)
        QtCore.QObject.connect(self.signalShowButton,QtCore.SIGNAL("toggled(bool)"),self.signalLabel.setEnabled)
        QtCore.QObject.connect(self.runStopButton,QtCore.SIGNAL("toggled(bool)"),self.speedFrame.setDisabled)
        QtCore.QObject.connect(self.runStopButton,QtCore.SIGNAL("toggled(bool)"),self.signalFrame.setDisabled)
        QtCore.QObject.connect(self.compValueButton,QtCore.SIGNAL("toggled(bool)"),self.resetButton.setEnabled)
        QtCore.QObject.connect(self.compValueButton,QtCore.SIGNAL("toggled(bool)"),self.stepButton.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(TimeSignalWidget)

    def retranslateUi(self, TimeSignalWidget):
        TimeSignalWidget.setWindowTitle(QtGui.QApplication.translate("TimeSignalWidget", "Time signal generator", None, QtGui.QApplication.UnicodeUTF8))
        self.runStopButton.setText(QtGui.QApplication.translate("TimeSignalWidget", "Run!", None, QtGui.QApplication.UnicodeUTF8))
        self.stepButton.setText(QtGui.QApplication.translate("TimeSignalWidget", "Step", None, QtGui.QApplication.UnicodeUTF8))
        self.resetButton.setText(QtGui.QApplication.translate("TimeSignalWidget", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.speedFrame.setTitle(QtGui.QApplication.translate("TimeSignalWidget", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.frequencyInput.setSuffix(QtGui.QApplication.translate("TimeSignalWidget", " Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.stepSizeInput.setSuffix(QtGui.QApplication.translate("TimeSignalWidget", " s", None, QtGui.QApplication.UnicodeUTF8))
        self.frequencyLabel.setText(QtGui.QApplication.translate("TimeSignalWidget", "Frequency:", None, QtGui.QApplication.UnicodeUTF8))
        self.stepSizeLabel.setText(QtGui.QApplication.translate("TimeSignalWidget", "Step size:", None, QtGui.QApplication.UnicodeUTF8))
        self.signalFrame.setTitle(QtGui.QApplication.translate("TimeSignalWidget", "Time signal", None, QtGui.QApplication.UnicodeUTF8))
        self.startValueLabel.setText(QtGui.QApplication.translate("TimeSignalWidget", "Start value:", None, QtGui.QApplication.UnicodeUTF8))
        self.compValueButton.setText(QtGui.QApplication.translate("TimeSignalWidget", "Computed value", None, QtGui.QApplication.UnicodeUTF8))
        self.stepLabel.setText(QtGui.QApplication.translate("TimeSignalWidget", "Step:", None, QtGui.QApplication.UnicodeUTF8))
        self.signalRatioLabel.setText(QtGui.QApplication.translate("TimeSignalWidget", "(10.0 x)", None, QtGui.QApplication.UnicodeUTF8))
        self.realTimeButton.setText(QtGui.QApplication.translate("TimeSignalWidget", "Realtime", None, QtGui.QApplication.UnicodeUTF8))
        self.signalFrame1.setTitle(QtGui.QApplication.translate("TimeSignalWidget", "Signal", None, QtGui.QApplication.UnicodeUTF8))
        self.signalLabel.setText(QtGui.QApplication.translate("TimeSignalWidget", "--", None, QtGui.QApplication.UnicodeUTF8))
        self.signalShowButton.setText(QtGui.QApplication.translate("TimeSignalWidget", "show", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    TimeSignalWidget = QtGui.QWidget()
    ui = Ui_TimeSignalWidget()
    ui.setupUi(TimeSignalWidget)
    TimeSignalWidget.show()
    sys.exit(app.exec_())
