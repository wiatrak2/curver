# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curver/ui/curve_join.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_curveEditWindow(object):
    def setupUi(self, curveEditWindow):
        curveEditWindow.setObjectName("curveEditWindow")
        curveEditWindow.resize(200, 650)
        self.curvesList = QtWidgets.QListWidget(curveEditWindow)
        self.curvesList.setGeometry(QtCore.QRect(10, 50, 180, 260))
        self.curvesList.setObjectName("curvesList")
        self.doneButton = QtWidgets.QPushButton(curveEditWindow)
        self.doneButton.setGeometry(QtCore.QRect(30, 500, 140, 30))
        self.doneButton.setObjectName("doneButton")
        self.moveToFirstButton = QtWidgets.QPushButton(curveEditWindow)
        self.moveToFirstButton.setGeometry(QtCore.QRect(30, 320, 140, 30))
        self.moveToFirstButton.setObjectName("moveToFirstButton")
        self.splitCurveButton = QtWidgets.QPushButton(curveEditWindow)
        self.splitCurveButton.setGeometry(QtCore.QRect(30, 410, 140, 30))
        self.splitCurveButton.setObjectName("splitCurveButton")
        self.mergeButton = QtWidgets.QPushButton(curveEditWindow)
        self.mergeButton.setGeometry(QtCore.QRect(30, 350, 140, 30))
        self.mergeButton.setObjectName("mergeButton")

        self.retranslateUi(curveEditWindow)
        QtCore.QMetaObject.connectSlotsByName(curveEditWindow)

    def retranslateUi(self, curveEditWindow):
        _translate = QtCore.QCoreApplication.translate
        curveEditWindow.setWindowTitle(_translate("curveEditWindow", "Form"))
        self.doneButton.setText(_translate("curveEditWindow", "Done"))
        self.moveToFirstButton.setText(_translate("curveEditWindow", "Move to first point"))
        self.splitCurveButton.setText(_translate("curveEditWindow", "Split Curve"))
        self.mergeButton.setText(_translate("curveEditWindow", "Merge"))
