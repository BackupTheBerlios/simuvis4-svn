# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SimuVis4/UI/ExceptionDialog.ui'
#
# Created: Wed Jan 23 08:58:18 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ExceptionDialog(object):
    def setupUi(self, ExceptionDialog):
        ExceptionDialog.setObjectName("ExceptionDialog")
        ExceptionDialog.resize(QtCore.QSize(QtCore.QRect(0,0,734,341).size()).expandedTo(ExceptionDialog.minimumSizeHint()))
        ExceptionDialog.setSizeGripEnabled(False)
        ExceptionDialog.setModal(True)

        self.vboxlayout = QtGui.QVBoxLayout(ExceptionDialog)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        self.IconLabel = QtGui.QLabel(ExceptionDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IconLabel.sizePolicy().hasHeightForWidth())
        self.IconLabel.setSizePolicy(sizePolicy)
        self.IconLabel.setObjectName("IconLabel")
        self.hboxlayout.addWidget(self.IconLabel)

        self.MainLabel = QtGui.QLabel(ExceptionDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainLabel.sizePolicy().hasHeightForWidth())
        self.MainLabel.setSizePolicy(sizePolicy)
        self.MainLabel.setWordWrap(True)
        self.MainLabel.setObjectName("MainLabel")
        self.hboxlayout.addWidget(self.MainLabel)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.TracebackView = QtGui.QTextBrowser(ExceptionDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.TracebackView.sizePolicy().hasHeightForWidth())
        self.TracebackView.setSizePolicy(sizePolicy)
        self.TracebackView.setObjectName("TracebackView")
        self.vboxlayout.addWidget(self.TracebackView)

        self.Iconlabel = QtGui.QLabel(ExceptionDialog)
        self.Iconlabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.Iconlabel.setWordWrap(True)
        self.Iconlabel.setObjectName("Iconlabel")
        self.vboxlayout.addWidget(self.Iconlabel)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(101,29,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.ExitButton = QtGui.QPushButton(ExceptionDialog)
        self.ExitButton.setObjectName("ExitButton")
        self.hboxlayout1.addWidget(self.ExitButton)

        self.KillButton = QtGui.QPushButton(ExceptionDialog)
        self.KillButton.setObjectName("KillButton")
        self.hboxlayout1.addWidget(self.KillButton)

        self.RestartButton = QtGui.QPushButton(ExceptionDialog)
        self.RestartButton.setObjectName("RestartButton")
        self.hboxlayout1.addWidget(self.RestartButton)

        self.IgnoreButton = QtGui.QPushButton(ExceptionDialog)
        self.IgnoreButton.setDefault(True)
        self.IgnoreButton.setObjectName("IgnoreButton")
        self.hboxlayout1.addWidget(self.IgnoreButton)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(ExceptionDialog)
        QtCore.QObject.connect(self.IgnoreButton,QtCore.SIGNAL("pressed()"),ExceptionDialog.close)
        QtCore.QMetaObject.connectSlotsByName(ExceptionDialog)
        ExceptionDialog.setTabOrder(self.IgnoreButton,self.ExitButton)
        ExceptionDialog.setTabOrder(self.ExitButton,self.KillButton)
        ExceptionDialog.setTabOrder(self.KillButton,self.RestartButton)

    def retranslateUi(self, ExceptionDialog):
        ExceptionDialog.setWindowTitle(QtGui.QApplication.translate("ExceptionDialog", "Python Exception", None, QtGui.QApplication.UnicodeUTF8))
        self.IconLabel.setText(QtGui.QApplication.translate("ExceptionDialog", "Icon", None, QtGui.QApplication.UnicodeUTF8))
        self.MainLabel.setText(QtGui.QApplication.translate("ExceptionDialog", "Exception", None, QtGui.QApplication.UnicodeUTF8))
        self.Iconlabel.setText(QtGui.QApplication.translate("ExceptionDialog", "Python exceptions are usually caused be bugs in the program code or unusual application conditions. The exception may be there because of a bug introduced by the SimuVis author, a bug in your own code or in the code of a plugin. \n"
        "Depending on the kind of exception you may simply ignore it, but it\'s safer to exit or restart the application.", None, QtGui.QApplication.UnicodeUTF8))
        self.ExitButton.setText(QtGui.QApplication.translate("ExceptionDialog", "Exit program", None, QtGui.QApplication.UnicodeUTF8))
        self.KillButton.setText(QtGui.QApplication.translate("ExceptionDialog", "Kill program", None, QtGui.QApplication.UnicodeUTF8))
        self.RestartButton.setText(QtGui.QApplication.translate("ExceptionDialog", "Restart program", None, QtGui.QApplication.UnicodeUTF8))
        self.IgnoreButton.setText(QtGui.QApplication.translate("ExceptionDialog", "Ignore", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ExceptionDialog = QtGui.QDialog()
    ui = Ui_ExceptionDialog()
    ui.setupUi(ExceptionDialog)
    ExceptionDialog.show()
    sys.exit(app.exec_())
