# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/curve_edit.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_curveEditWindow(object):
    def setupUi(self, curveEditWindow):
        curveEditWindow.setObjectName("curveEditWindow")
        curveEditWindow.resize(383, 407)
        self.vectorMoveButton = QtWidgets.QPushButton(curveEditWindow)
        self.vectorMoveButton.setGeometry(QtCore.QRect(10, 130, 121, 32))
        self.vectorMoveButton.setObjectName("vectorMoveButton")
        self.doneButton = QtWidgets.QPushButton(curveEditWindow)
        self.doneButton.setGeometry(QtCore.QRect(250, 360, 113, 32))
        self.doneButton.setObjectName("doneButton")
        self.curveName = QtWidgets.QLineEdit(curveEditWindow)
        self.curveName.setEnabled(True)
        self.curveName.setGeometry(QtCore.QRect(30, 10, 321, 31))
        self.curveName.setObjectName("curveName")
        self.vectorMoveBox = QtWidgets.QGroupBox(curveEditWindow)
        self.vectorMoveBox.setGeometry(QtCore.QRect(130, 100, 221, 61))
        self.vectorMoveBox.setObjectName("vectorMoveBox")
        self.xPos = QtWidgets.QLineEdit(self.vectorMoveBox)
        self.xPos.setGeometry(QtCore.QRect(0, 30, 41, 31))
        self.xPos.setInputMethodHints(QtCore.Qt.ImhNone)
        self.xPos.setObjectName("xPos")
        self.yPos = QtWidgets.QLineEdit(self.vectorMoveBox)
        self.yPos.setGeometry(QtCore.QRect(60, 30, 41, 31))
        self.yPos.setInputMethodHints(QtCore.Qt.ImhNone)
        self.yPos.setObjectName("yPos")
        self.moveButton = QtWidgets.QPushButton(self.vectorMoveBox)
        self.moveButton.setGeometry(QtCore.QRect(110, 30, 113, 32))
        self.moveButton.setObjectName("moveButton")
        self.cancelButton = QtWidgets.QPushButton(curveEditWindow)
        self.cancelButton.setGeometry(QtCore.QRect(250, 320, 113, 32))
        self.cancelButton.setObjectName("cancelButton")
        self.permutePointsButton = QtWidgets.QPushButton(curveEditWindow)
        self.permutePointsButton.setGeometry(QtCore.QRect(10, 170, 121, 32))
        self.permutePointsButton.setObjectName("permutePointsButton")
        self.rotateCurveButton = QtWidgets.QPushButton(curveEditWindow)
        self.rotateCurveButton.setGeometry(QtCore.QRect(10, 210, 121, 32))
        self.rotateCurveButton.setObjectName("rotateCurveButton")
        self.rotateCurveBox = QtWidgets.QGroupBox(curveEditWindow)
        self.rotateCurveBox.setGeometry(QtCore.QRect(130, 180, 191, 61))
        self.rotateCurveBox.setObjectName("rotateCurveBox")
        self.angle = QtWidgets.QLineEdit(self.rotateCurveBox)
        self.angle.setGeometry(QtCore.QRect(30, 30, 41, 31))
        self.angle.setInputMethodHints(QtCore.Qt.ImhNone)
        self.angle.setObjectName("angle")
        self.rotateButton = QtWidgets.QPushButton(self.rotateCurveBox)
        self.rotateButton.setGeometry(QtCore.QRect(80, 30, 113, 32))
        self.rotateButton.setObjectName("rotateButton")
        self.scaleCurveButton = QtWidgets.QPushButton(curveEditWindow)
        self.scaleCurveButton.setGeometry(QtCore.QRect(10, 250, 121, 32))
        self.scaleCurveButton.setObjectName("scaleCurveButton")
        self.deletePointButton = QtWidgets.QPushButton(curveEditWindow)
        self.deletePointButton.setGeometry(QtCore.QRect(10, 90, 121, 32))
        self.deletePointButton.setObjectName("deletePointButton")
        self.addPointButton = QtWidgets.QPushButton(curveEditWindow)
        self.addPointButton.setGeometry(QtCore.QRect(10, 50, 121, 32))
        self.addPointButton.setObjectName("addPointButton")
        self.exportCurveButton = QtWidgets.QPushButton(curveEditWindow)
        self.exportCurveButton.setGeometry(QtCore.QRect(10, 290, 121, 32))
        self.exportCurveButton.setObjectName("exportCurveButton")
        self.undoButton = QtWidgets.QPushButton(curveEditWindow)
        self.undoButton.setGeometry(QtCore.QRect(10, 360, 121, 32))
        self.undoButton.setObjectName("undoButton")
        self.scaleCurveBox = QtWidgets.QGroupBox(curveEditWindow)
        self.scaleCurveBox.setGeometry(QtCore.QRect(130, 230, 191, 61))
        self.scaleCurveBox.setObjectName("scaleCurveBox")
        self.scaleValue = QtWidgets.QLineEdit(self.scaleCurveBox)
        self.scaleValue.setGeometry(QtCore.QRect(30, 30, 41, 31))
        self.scaleValue.setInputMethodHints(QtCore.Qt.ImhNone)
        self.scaleValue.setObjectName("scaleValue")
        self.scaleButton = QtWidgets.QPushButton(self.scaleCurveBox)
        self.scaleButton.setGeometry(QtCore.QRect(80, 30, 113, 32))
        self.scaleButton.setObjectName("scaleButton")

        self.retranslateUi(curveEditWindow)
        QtCore.QMetaObject.connectSlotsByName(curveEditWindow)

    def retranslateUi(self, curveEditWindow):
        _translate = QtCore.QCoreApplication.translate
        curveEditWindow.setWindowTitle(_translate("curveEditWindow", "Form"))
        self.vectorMoveButton.setText(_translate("curveEditWindow", "Move by vector"))
        self.doneButton.setText(_translate("curveEditWindow", "Done"))
        self.vectorMoveBox.setTitle(_translate("curveEditWindow", "vectorMoveBox"))
        self.moveButton.setText(_translate("curveEditWindow", "Move"))
        self.cancelButton.setText(_translate("curveEditWindow", "Cancel"))
        self.permutePointsButton.setText(_translate("curveEditWindow", "Permute points"))
        self.rotateCurveButton.setText(_translate("curveEditWindow", "Rotate by angle"))
        self.rotateCurveBox.setTitle(_translate("curveEditWindow", "rotateBox"))
        self.rotateButton.setText(_translate("curveEditWindow", "Rotate"))
        self.scaleCurveButton.setText(_translate("curveEditWindow", "Scale"))
        self.deletePointButton.setText(_translate("curveEditWindow", "Delete point"))
        self.addPointButton.setText(_translate("curveEditWindow", "Add point"))
        self.exportCurveButton.setText(_translate("curveEditWindow", "Export"))
        self.undoButton.setText(_translate("curveEditWindow", "Undo"))
        self.scaleCurveBox.setTitle(_translate("curveEditWindow", "scaleBox"))
        self.scaleButton.setText(_translate("curveEditWindow", "Scale"))
