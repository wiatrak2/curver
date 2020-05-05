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
        self.cancelButton = QtWidgets.QPushButton(curveEditWindow)
        self.cancelButton.setGeometry(QtCore.QRect(220, 210, 140, 32))
        self.cancelButton.setObjectName("cancelButton")
        self.doneButton = QtWidgets.QPushButton(curveEditWindow)
        self.doneButton.setGeometry(QtCore.QRect(220, 240, 140, 32))
        self.doneButton.setObjectName("doneButton")
        self.moveToFirstButton = QtWidgets.QPushButton(curveEditWindow)
        self.moveToFirstButton.setGeometry(QtCore.QRect(220, 40, 140, 32))
        self.moveToFirstButton.setObjectName("moveToFirstButton")
        self.moveToLastButton = QtWidgets.QPushButton(curveEditWindow)
        self.moveToLastButton.setGeometry(QtCore.QRect(220, 70, 140, 32))
        self.moveToLastButton.setObjectName("moveToLastButton")
        self.mergeRightButton = QtWidgets.QPushButton(curveEditWindow)
        self.mergeRightButton.setGeometry(QtCore.QRect(220, 130, 140, 32))
        self.mergeRightButton.setObjectName("mergeRightButton")
        self.mergeLeftButton = QtWidgets.QPushButton(curveEditWindow)
        self.mergeLeftButton.setGeometry(QtCore.QRect(220, 100, 140, 32))
        self.mergeLeftButton.setObjectName("mergeLeftButton")

        self.retranslateUi(curveEditWindow)
        QtCore.QMetaObject.connectSlotsByName(curveEditWindow)

    def retranslateUi(self, curveEditWindow):
        _translate = QtCore.QCoreApplication.translate
        curveEditWindow.setWindowTitle(_translate("curveEditWindow", "Form"))
        self.cancelButton.setText(_translate("curveEditWindow", "Cancel"))
        self.doneButton.setText(_translate("curveEditWindow", "Done"))
        self.moveToFirstButton.setText(
            _translate("curveEditWindow", "Move to first point")
        )
        self.moveToLastButton.setText(
            _translate("curveEditWindow", "Move to last point")
        )
        self.mergeRightButton.setText(_translate("curveEditWindow", "Merge as right"))
        self.mergeLeftButton.setText(_translate("curveEditWindow", "Merge as left"))
