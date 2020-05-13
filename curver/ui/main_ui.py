# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curver/ui/main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1088, 728)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 30, 1051, 651))
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1088, 22))
        self.menubar.setObjectName("menubar")
        self.menutopbar = QtWidgets.QMenu(self.menubar)
        self.menutopbar.setObjectName("menutopbar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.actionImportCurve = QtWidgets.QAction(MainWindow)
        self.actionImportCurve.setObjectName("actionImportCurve")
        self.actionChangeColor = QtWidgets.QAction(MainWindow)
        self.actionChangeColor.setObjectName("actionChangeColor")
        self.menutopbar.addSeparator()
        self.menutopbar.addAction(self.actionImportCurve)
        self.menuEdit.addAction(self.actionChangeColor)
        self.menubar.addAction(self.menutopbar.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menutopbar.setTitle(_translate("MainWindow", "Menu"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionImportCurve.setText(_translate("MainWindow", "Import curve"))
        self.actionChangeColor.setText(_translate("MainWindow", "Change color"))
