# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(851, 622)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plane = QtWidgets.QGraphicsView(self.centralwidget)
        self.plane.setGeometry(QtCore.QRect(190, 20, 631, 541))
        self.plane.setObjectName("plane")
        self.addCurveButton = QtWidgets.QPushButton(self.centralwidget)
        self.addCurveButton.setGeometry(QtCore.QRect(20, 80, 113, 32))
        self.addCurveButton.setObjectName("addCurveButton")
        self.setCurveType = QtWidgets.QComboBox(self.centralwidget)
        self.setCurveType.setGeometry(QtCore.QRect(30, 40, 104, 26))
        self.setCurveType.setObjectName("setCurveType")
        self.setCurveType.addItem("")
        self.addPointBox = QtWidgets.QGroupBox(self.centralwidget)
        self.addPointBox.setEnabled(True)
        self.addPointBox.setGeometry(QtCore.QRect(20, 140, 131, 251))
        self.addPointBox.setTitle("")
        self.addPointBox.setObjectName("addPointBox")
        self.xPos = QtWidgets.QLineEdit(self.addPointBox)
        self.xPos.setGeometry(QtCore.QRect(20, 60, 41, 31))
        self.xPos.setInputMethodHints(QtCore.Qt.ImhNone)
        self.xPos.setObjectName("xPos")
        self.yPos = QtWidgets.QLineEdit(self.addPointBox)
        self.yPos.setEnabled(True)
        self.yPos.setGeometry(QtCore.QRect(70, 60, 41, 31))
        self.yPos.setObjectName("yPos")
        self.addPointButton = QtWidgets.QPushButton(self.addPointBox)
        self.addPointButton.setGeometry(QtCore.QRect(10, 100, 113, 32))
        self.addPointButton.setObjectName("addPointButton")
        self.saveCurveButton = QtWidgets.QPushButton(self.addPointBox)
        self.saveCurveButton.setGeometry(QtCore.QRect(10, 220, 113, 32))
        self.saveCurveButton.setObjectName("saveCurveButton")
        self.curveName = QtWidgets.QLineEdit(self.addPointBox)
        self.curveName.setEnabled(True)
        self.curveName.setGeometry(QtCore.QRect(20, 20, 101, 31))
        self.curveName.setObjectName("curveName")
        self.undoAddPointButton = QtWidgets.QPushButton(self.addPointBox)
        self.undoAddPointButton.setGeometry(QtCore.QRect(10, 130, 113, 32))
        self.undoAddPointButton.setObjectName("undoAddPointButton")
        self.cancelAddCurveButton = QtWidgets.QPushButton(self.addPointBox)
        self.cancelAddCurveButton.setGeometry(QtCore.QRect(10, 190, 113, 32))
        self.cancelAddCurveButton.setObjectName("cancelAddCurveButton")
        self.editCurveButton = QtWidgets.QPushButton(self.centralwidget)
        self.editCurveButton.setGeometry(QtCore.QRect(30, 460, 113, 32))
        self.editCurveButton.setObjectName("editCurveButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 851, 22))
        self.menubar.setObjectName("menubar")
        self.menutopbar = QtWidgets.QMenu(self.menubar)
        self.menutopbar.setObjectName("menutopbar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menutopbar.addSeparator()
        self.menubar.addAction(self.menutopbar.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addCurveButton.setText(_translate("MainWindow", "Add Curve"))
        self.setCurveType.setItemText(0, _translate("MainWindow", "Polyline"))
        self.addPointButton.setText(_translate("MainWindow", "Add Point"))
        self.saveCurveButton.setText(_translate("MainWindow", "Done"))
        self.undoAddPointButton.setText(_translate("MainWindow", "Undo"))
        self.cancelAddCurveButton.setText(_translate("MainWindow", "Cancel"))
        self.editCurveButton.setText(_translate("MainWindow", "Edit Curve"))
        self.menutopbar.setTitle(_translate("MainWindow", "topbar"))
