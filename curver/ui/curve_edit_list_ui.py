# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curver/ui/curve_edit_list.ui'
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
        self.curveEditButton = QtWidgets.QPushButton(curveEditWindow)
        self.curveEditButton.setGeometry(QtCore.QRect(30, 380, 140, 30))
        self.curveEditButton.setObjectName("curveEditButton")
        self.curveDeleteButton = QtWidgets.QPushButton(curveEditWindow)
        self.curveDeleteButton.setGeometry(QtCore.QRect(30, 410, 140, 30))
        self.curveDeleteButton.setObjectName("curveDeleteButton")
        self.doneButton = QtWidgets.QPushButton(curveEditWindow)
        self.doneButton.setGeometry(QtCore.QRect(30, 500, 140, 30))
        self.doneButton.setObjectName("doneButton")
        self.changeCurveVisibilityButton = QtWidgets.QPushButton(curveEditWindow)
        self.changeCurveVisibilityButton.setGeometry(QtCore.QRect(30, 320, 140, 30))
        self.changeCurveVisibilityButton.setObjectName("changeCurveVisibilityButton")
        self.changePointsVisibilityButton = QtWidgets.QPushButton(curveEditWindow)
        self.changePointsVisibilityButton.setGeometry(QtCore.QRect(30, 350, 140, 30))
        self.changePointsVisibilityButton.setObjectName("changePointsVisibilityButton")

        self.retranslateUi(curveEditWindow)
        QtCore.QMetaObject.connectSlotsByName(curveEditWindow)

    def retranslateUi(self, curveEditWindow):
        _translate = QtCore.QCoreApplication.translate
        curveEditWindow.setWindowTitle(_translate("curveEditWindow", "Form"))
        self.curveEditButton.setText(_translate("curveEditWindow", "Edit"))
        self.curveDeleteButton.setText(_translate("curveEditWindow", "Delete"))
        self.doneButton.setText(_translate("curveEditWindow", "Done"))
        self.changeCurveVisibilityButton.setText(
            _translate("curveEditWindow", "Show/Hide")
        )
        self.changePointsVisibilityButton.setText(
            _translate("curveEditWindow", "Show/Hide Points")
        )
