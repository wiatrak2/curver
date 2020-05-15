# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curver/ui/main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Curver(object):
    def setupUi(self, Curver):
        Curver.setObjectName("Curver")
        Curver.resize(1107, 728)
        self.centralwidget = QtWidgets.QWidget(Curver)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 1101, 661))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.mainLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setObjectName("mainLayout")
        self.plane = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.plane.setObjectName("plane")
        self.mainLayout.addWidget(self.plane, 0, 1, 1, 1)
        self.panelLayout = QtWidgets.QVBoxLayout()
        self.panelLayout.setObjectName("panelLayout")
        self.mainLayout.addLayout(self.panelLayout, 0, 0, 1, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 5)
        Curver.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Curver)
        self.statusbar.setObjectName("statusbar")
        Curver.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(Curver)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1107, 22))
        self.menubar.setObjectName("menubar")
        self.menutopbar = QtWidgets.QMenu(self.menubar)
        self.menutopbar.setObjectName("menutopbar")
        Curver.setMenuBar(self.menubar)
        self.actionImportCurve = QtWidgets.QAction(Curver)
        self.actionImportCurve.setObjectName("actionImportCurve")
        self.actionChangeColor = QtWidgets.QAction(Curver)
        self.actionChangeColor.setObjectName("actionChangeColor")
        self.menutopbar.addSeparator()
        self.menutopbar.addAction(self.actionImportCurve)
        self.menubar.addAction(self.menutopbar.menuAction())

        self.retranslateUi(Curver)
        QtCore.QMetaObject.connectSlotsByName(Curver)

    def retranslateUi(self, Curver):
        _translate = QtCore.QCoreApplication.translate
        Curver.setWindowTitle(_translate("Curver", "Curver"))
        self.menutopbar.setTitle(_translate("Curver", "Menu"))
        self.actionImportCurve.setText(_translate("Curver", "Import curve"))
        self.actionChangeColor.setText(_translate("Curver", "Change color"))
