# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SimuVis4/UI/HelpBrowser.ui'
#
# Created: Tue Mar 20 13:13:17 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_HelpBrowserWidget(object):
    def setupUi(self, HelpBrowserWidget):
        HelpBrowserWidget.setObjectName("HelpBrowserWidget")
        HelpBrowserWidget.resize(QtCore.QSize(QtCore.QRect(0,0,438,392).size()).expandedTo(HelpBrowserWidget.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(HelpBrowserWidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter = QtGui.QSplitter(HelpBrowserWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.topicTree = QtGui.QTreeWidget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topicTree.sizePolicy().hasHeightForWidth())
        self.topicTree.setSizePolicy(sizePolicy)
        self.topicTree.setIndentation(10)
        self.topicTree.setRootIsDecorated(False)
        self.topicTree.setObjectName("topicTree")

        self.textBrowser = QtGui.QTextBrowser(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(300,0))
        self.textBrowser.setObjectName("textBrowser")
        self.vboxlayout.addWidget(self.splitter)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.closeButton = QtGui.QPushButton(HelpBrowserWidget)
        self.closeButton.setObjectName("closeButton")
        self.hboxlayout.addWidget(self.closeButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(HelpBrowserWidget)
        QtCore.QMetaObject.connectSlotsByName(HelpBrowserWidget)

    def retranslateUi(self, HelpBrowserWidget):
        HelpBrowserWidget.setWindowTitle(QtGui.QApplication.translate("HelpBrowserWidget", "Help Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.topicTree.headerItem().setText(0,QtGui.QApplication.translate("HelpBrowserWidget", "Topic", None, QtGui.QApplication.UnicodeUTF8))
        self.topicTree.clear()

        item = QtGui.QTreeWidgetItem(self.topicTree)
        item.setText(0,QtGui.QApplication.translate("HelpBrowserWidget", "SimuVis4", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("HelpBrowserWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    HelpBrowserWidget = QtGui.QWidget()
    ui = Ui_HelpBrowserWidget()
    ui.setupUi(HelpBrowserWidget)
    HelpBrowserWidget.show()
    sys.exit(app.exec_())
