# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SimuVis4/UI/AboutDialog.ui'
#
# Created: Mon Feb 12 22:37:01 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(QtCore.QSize(QtCore.QRect(0,0,576,296).size()).expandedTo(AboutDialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(AboutDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.TabView = QtGui.QTabWidget(AboutDialog)
        self.TabView.setObjectName("TabView")

        self.TabAbout = QtGui.QWidget()
        self.TabAbout.setObjectName("TabAbout")

        self.hboxlayout = QtGui.QHBoxLayout(self.TabAbout)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.AboutPicture = QtGui.QLabel(self.TabAbout)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AboutPicture.sizePolicy().hasHeightForWidth())
        self.AboutPicture.setSizePolicy(sizePolicy)
        self.AboutPicture.setObjectName("AboutPicture")
        self.hboxlayout.addWidget(self.AboutPicture)

        self.AboutText = QtGui.QLabel(self.TabAbout)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AboutText.sizePolicy().hasHeightForWidth())
        self.AboutText.setSizePolicy(sizePolicy)
        self.AboutText.setObjectName("AboutText")
        self.hboxlayout.addWidget(self.AboutText)
        self.TabView.addTab(self.TabAbout,"")

        self.TabLicense = QtGui.QWidget()
        self.TabLicense.setObjectName("TabLicense")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.TabLicense)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.LicenseView = QtGui.QTextEdit(self.TabLicense)
        self.LicenseView.setReadOnly(True)
        self.LicenseView.setObjectName("LicenseView")
        self.hboxlayout1.addWidget(self.LicenseView)
        self.TabView.addTab(self.TabLicense,"")

        self.TabAuthors = QtGui.QWidget()
        self.TabAuthors.setObjectName("TabAuthors")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.TabAuthors)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.AuthorsView = QtGui.QLabel(self.TabAuthors)
        self.AuthorsView.setObjectName("AuthorsView")
        self.vboxlayout1.addWidget(self.AuthorsView)
        self.TabView.addTab(self.TabAuthors,"")

        self.TabVersions = QtGui.QWidget()
        self.TabVersions.setObjectName("TabVersions")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.TabVersions)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.VersionView = QtGui.QTextEdit(self.TabVersions)
        self.VersionView.setReadOnly(True)
        self.VersionView.setObjectName("VersionView")
        self.vboxlayout2.addWidget(self.VersionView)
        self.TabView.addTab(self.TabVersions,"")
        self.vboxlayout.addWidget(self.TabView)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem = QtGui.QSpacerItem(131,31,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem)

        self.okButton = QtGui.QPushButton(AboutDialog)
        self.okButton.setObjectName("okButton")
        self.hboxlayout2.addWidget(self.okButton)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(AboutDialog)
        self.TabView.setCurrentIndex(0)
        QtCore.QObject.connect(self.okButton,QtCore.SIGNAL("clicked()"),AboutDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.AboutPicture.setText(QtGui.QApplication.translate("AboutDialog", "Picture", None, QtGui.QApplication.UnicodeUTF8))
        self.AboutText.setText(QtGui.QApplication.translate("AboutDialog", "Text", None, QtGui.QApplication.UnicodeUTF8))
        self.TabView.setTabText(self.TabView.indexOf(self.TabAbout), QtGui.QApplication.translate("AboutDialog", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.TabView.setTabText(self.TabView.indexOf(self.TabLicense), QtGui.QApplication.translate("AboutDialog", "&License", None, QtGui.QApplication.UnicodeUTF8))
        self.TabView.setTabText(self.TabView.indexOf(self.TabAuthors), QtGui.QApplication.translate("AboutDialog", "A&uthors", None, QtGui.QApplication.UnicodeUTF8))
        self.TabView.setTabText(self.TabView.indexOf(self.TabVersions), QtGui.QApplication.translate("AboutDialog", "&Versions", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("AboutDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    AboutDialog = QtGui.QDialog()
    ui = Ui_AboutDialog()
    ui.setupUi(AboutDialog)
    AboutDialog.show()
    sys.exit(app.exec_())
