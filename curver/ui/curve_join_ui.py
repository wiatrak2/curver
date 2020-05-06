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
        curveEditWindow.resize(400, 300)
        self.curvesList = QtWidgets.QListWidget(curveEditWindow)
        self.curvesList.setGeometry(QtCore.QRect(10, 10, 181, 261))
        self.curvesList.setObjectName("curvesList")
        self.doneButton = QtWidgets.QPushButton(curveEditWindow)
        self.doneButton.setGeometry(QtCore.QRect(220, 240, 140, 32))
        self.doneButton.setObjectName("doneButton")
        self.moveToFirstButton = QtWidgets.QPushButton(curveEditWindow)
        self.moveToFirstButton.setGeometry(QtCore.QRect(220, 40, 140, 32))
        self.moveToFirstButton.setObjectName("moveToFirstButton")
        self.moveToLastButton = QtWidgets.QPushButton(curveEditWindow)
        self.moveToLastButton.setGeometry(QtCore.QRect(220, 70, 140, 32))
        self.moveToLastButton.setObjectName("moveToLastButton")
        self.splitCurveButton = QtWidgets.QPushButton(curveEditWindow)
        self.splitCurveButton.setGeometry(QtCore.QRect(220, 170, 140, 32))
        self.splitCurveButton.setObjectName("splitCurveButton")
        self.mergeButton = QtWidgets.QPushButton(curveEditWindow)
        self.mergeButton.setGeometry(QtCore.QRect(220, 100, 140, 32))
        self.mergeButton.setObjectName("mergeButton")

        self.retranslateUi(curveEditWindow)
        QtCore.QMetaObject.connectSlotsByName(curveEditWindow)

    def retranslateUi(self, curveEditWindow):
        _translate = QtCore.QCoreApplication.translate
        curveEditWindow.setWindowTitle(_translate("curveEditWindow", "Form"))
        self.doneButton.setText(_translate("curveEditWindow", "Done"))
        self.moveToFirstButton.setText(_translate("curveEditWindow", "Move to first point"))
        self.moveToLastButton.setText(_translate("curveEditWindow", "Move to last point"))
        self.splitCurveButton.setText(_translate("curveEditWindow", "Split Curve"))
        self.mergeButton.setText(_translate("curveEditWindow", "Merge"))
