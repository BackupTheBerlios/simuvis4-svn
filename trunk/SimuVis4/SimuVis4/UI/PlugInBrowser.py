# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SimuVis4/UI/PlugInBrowser.ui'
#
# Created: Mon Feb 12 22:56:25 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_PlugInBrowserWidget(object):
    def setupUi(self, PlugInBrowserWidget):
        PlugInBrowserWidget.setObjectName("PlugInBrowserWidget")
        PlugInBrowserWidget.resize(QtCore.QSize(QtCore.QRect(0,0,628,247).size()).expandedTo(PlugInBrowserWidget.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PlugInBrowserWidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.PlugInView = QtGui.QTreeWidget(PlugInBrowserWidget)
        self.PlugInView.setRootIsDecorated(False)
        self.PlugInView.setObjectName("PlugInView")
        self.vboxlayout.addWidget(self.PlugInView)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(292,29,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.ActiveButton = QtGui.QPushButton(PlugInBrowserWidget)
        self.ActiveButton.setEnabled(False)
        self.ActiveButton.setObjectName("ActiveButton")
        self.hboxlayout.addWidget(self.ActiveButton)

        self.DeleteButton = QtGui.QPushButton(PlugInBrowserWidget)
        self.DeleteButton.setEnabled(False)
        self.DeleteButton.setObjectName("DeleteButton")
        self.hboxlayout.addWidget(self.DeleteButton)

        self.AddButton = QtGui.QPushButton(PlugInBrowserWidget)
        self.AddButton.setEnabled(False)
        self.AddButton.setObjectName("AddButton")
        self.hboxlayout.addWidget(self.AddButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(PlugInBrowserWidget)
        QtCore.QMetaObject.connectSlotsByName(PlugInBrowserWidget)

    def retranslateUi(self, PlugInBrowserWidget):
        PlugInBrowserWidget.setWindowTitle(QtGui.QApplication.translate("PlugInBrowserWidget", "PlugIns", None, QtGui.QApplication.UnicodeUTF8))
        self.PlugInView.headerItem().setText(0,QtGui.QApplication.translate("PlugInBrowserWidget", "State", None, QtGui.QApplication.UnicodeUTF8))
        self.PlugInView.headerItem().setText(1,QtGui.QApplication.translate("PlugInBrowserWidget", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.PlugInView.headerItem().setText(2,QtGui.QApplication.translate("PlugInBrowserWidget", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.PlugInView.headerItem().setText(3,QtGui.QApplication.translate("PlugInBrowserWidget", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.PlugInView.headerItem().setText(4,QtGui.QApplication.translate("PlugInBrowserWidget", "Path", None, QtGui.QApplication.UnicodeUTF8))
        self.ActiveButton.setText(QtGui.QApplication.translate("PlugInBrowserWidget", "Toggle Active", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteButton.setText(QtGui.QApplication.translate("PlugInBrowserWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.AddButton.setText(QtGui.QApplication.translate("PlugInBrowserWidget", "Add ...", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    PlugInBrowserWidget = QtGui.QWidget()
    ui = Ui_PlugInBrowserWidget()
    ui.setupUi(PlugInBrowserWidget)
    PlugInBrowserWidget.show()
    sys.exit(app.exec_())
