# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SimuVis4/UI/TaskBrowser.ui'
#
# Created: Wed Jan 24 11:13:41 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_TaskBrowserWidget(object):
    def setupUi(self, TaskBrowserWidget):
        TaskBrowserWidget.setObjectName("TaskBrowserWidget")
        TaskBrowserWidget.resize(QtCore.QSize(QtCore.QRect(0,0,595,290).size()).expandedTo(TaskBrowserWidget.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(TaskBrowserWidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.TaskView = QtGui.QTableWidget(TaskBrowserWidget)
        self.TaskView.setObjectName("TaskView")
        self.vboxlayout.addWidget(self.TaskView)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(307,29,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.StopButton = QtGui.QPushButton(TaskBrowserWidget)
        self.StopButton.setObjectName("StopButton")
        self.hboxlayout.addWidget(self.StopButton)

        self.DeleteButton = QtGui.QPushButton(TaskBrowserWidget)
        self.DeleteButton.setObjectName("DeleteButton")
        self.hboxlayout.addWidget(self.DeleteButton)

        self.ClearButton = QtGui.QPushButton(TaskBrowserWidget)
        self.ClearButton.setObjectName("ClearButton")
        self.hboxlayout.addWidget(self.ClearButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(TaskBrowserWidget)
        QtCore.QMetaObject.connectSlotsByName(TaskBrowserWidget)

    def retranslateUi(self, TaskBrowserWidget):
        TaskBrowserWidget.setWindowTitle(QtGui.QApplication.translate("TaskBrowserWidget", "Tasks", None, QtGui.QApplication.UnicodeUTF8))
        self.TaskView.clear()
        self.TaskView.setColumnCount(3)
        self.TaskView.setRowCount(0)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("TaskBrowserWidget", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.TaskView.setHorizontalHeaderItem(0,headerItem)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("TaskBrowserWidget", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.TaskView.setHorizontalHeaderItem(1,headerItem1)

        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("TaskBrowserWidget", "Started", None, QtGui.QApplication.UnicodeUTF8))
        self.TaskView.setHorizontalHeaderItem(2,headerItem2)
        self.StopButton.setText(QtGui.QApplication.translate("TaskBrowserWidget", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteButton.setText(QtGui.QApplication.translate("TaskBrowserWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearButton.setText(QtGui.QApplication.translate("TaskBrowserWidget", "Clear old", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    TaskBrowserWidget = QtGui.QWidget()
    ui = Ui_TaskBrowserWidget()
    ui.setupUi(TaskBrowserWidget)
    TaskBrowserWidget.show()
    sys.exit(app.exec_())
