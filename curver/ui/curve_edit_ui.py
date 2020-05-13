# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curver/ui/curve_edit.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_curveEditPanel(object):
    def setupUi(self, curveEditPanel):
        curveEditPanel.setObjectName("curveEditPanel")
        curveEditPanel.resize(200, 650)
        self.rotateCurveButton = QtWidgets.QPushButton(curveEditPanel)
        self.rotateCurveButton.setGeometry(QtCore.QRect(30, 260, 121, 32))
        self.rotateCurveButton.setObjectName("rotateCurveButton")
        self.scaleCurveBox = QtWidgets.QGroupBox(curveEditPanel)
        self.scaleCurveBox.setGeometry(QtCore.QRect(30, 450, 121, 61))
        self.scaleCurveBox.setTitle("")
        self.scaleCurveBox.setFlat(True)
        self.scaleCurveBox.setObjectName("scaleCurveBox")
        self.scaleDoneButton = QtWidgets.QPushButton(self.scaleCurveBox)
        self.scaleDoneButton.setGeometry(QtCore.QRect(20, 30, 71, 32))
        self.scaleDoneButton.setObjectName("scaleDoneButton")
        self.scaleSlider = QtWidgets.QSlider(self.scaleCurveBox)
        self.scaleSlider.setGeometry(QtCore.QRect(0, 0, 111, 22))
        self.scaleSlider.setSliderPosition(50)
        self.scaleSlider.setOrientation(QtCore.Qt.Horizontal)
        self.scaleSlider.setObjectName("scaleSlider")
        self.rotateCurveBox = QtWidgets.QGroupBox(curveEditPanel)
        self.rotateCurveBox.setGeometry(QtCore.QRect(30, 450, 121, 61))
        self.rotateCurveBox.setTitle("")
        self.rotateCurveBox.setFlat(True)
        self.rotateCurveBox.setObjectName("rotateCurveBox")
        self.rotateDoneButton = QtWidgets.QPushButton(self.rotateCurveBox)
        self.rotateDoneButton.setGeometry(QtCore.QRect(20, 30, 71, 32))
        self.rotateDoneButton.setObjectName("rotateDoneButton")
        self.rotationSlider = QtWidgets.QSlider(self.rotateCurveBox)
        self.rotationSlider.setGeometry(QtCore.QRect(0, 0, 111, 22))
        self.rotationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.rotationSlider.setObjectName("rotationSlider")
        self.addPointButton = QtWidgets.QPushButton(curveEditPanel)
        self.addPointButton.setGeometry(QtCore.QRect(30, 60, 121, 32))
        self.addPointButton.setObjectName("addPointButton")
        self.permutePointsButton = QtWidgets.QPushButton(curveEditPanel)
        self.permutePointsButton.setGeometry(QtCore.QRect(30, 180, 121, 32))
        self.permutePointsButton.setObjectName("permutePointsButton")
        self.editWeightBox = QtWidgets.QGroupBox(curveEditPanel)
        self.editWeightBox.setGeometry(QtCore.QRect(30, 400, 121, 31))
        self.editWeightBox.setTitle("")
        self.editWeightBox.setFlat(True)
        self.editWeightBox.setObjectName("editWeightBox")
        self.editWeightButton = QtWidgets.QPushButton(self.editWeightBox)
        self.editWeightButton.setGeometry(QtCore.QRect(0, 0, 121, 32))
        self.editWeightButton.setObjectName("editWeightButton")
        self.curveName = QtWidgets.QLineEdit(curveEditPanel)
        self.curveName.setEnabled(True)
        self.curveName.setGeometry(QtCore.QRect(20, 20, 141, 31))
        self.curveName.setObjectName("curveName")
        self.undoButton = QtWidgets.QPushButton(curveEditPanel)
        self.undoButton.setGeometry(QtCore.QRect(30, 550, 111, 32))
        self.undoButton.setObjectName("undoButton")
        self.exportCurveButton = QtWidgets.QPushButton(curveEditPanel)
        self.exportCurveButton.setGeometry(QtCore.QRect(30, 340, 121, 32))
        self.exportCurveButton.setObjectName("exportCurveButton")
        self.deletePointButton = QtWidgets.QPushButton(curveEditPanel)
        self.deletePointButton.setGeometry(QtCore.QRect(30, 100, 121, 32))
        self.deletePointButton.setObjectName("deletePointButton")
        self.addPointBox = QtWidgets.QGroupBox(curveEditPanel)
        self.addPointBox.setGeometry(QtCore.QRect(30, 450, 111, 81))
        self.addPointBox.setTitle("")
        self.addPointBox.setFlat(True)
        self.addPointBox.setObjectName("addPointBox")
        self.addXPos = QtWidgets.QLineEdit(self.addPointBox)
        self.addXPos.setGeometry(QtCore.QRect(10, 10, 40, 30))
        self.addXPos.setInputMethodHints(QtCore.Qt.ImhNone)
        self.addXPos.setObjectName("addXPos")
        self.addYPos = QtWidgets.QLineEdit(self.addPointBox)
        self.addYPos.setGeometry(QtCore.QRect(60, 10, 40, 30))
        self.addYPos.setInputMethodHints(QtCore.Qt.ImhNone)
        self.addYPos.setObjectName("addYPos")
        self.addButton = QtWidgets.QPushButton(self.addPointBox)
        self.addButton.setGeometry(QtCore.QRect(0, 40, 113, 32))
        self.addButton.setObjectName("addButton")
        self.vectorMoveBox = QtWidgets.QGroupBox(curveEditPanel)
        self.vectorMoveBox.setGeometry(QtCore.QRect(30, 450, 111, 81))
        self.vectorMoveBox.setTitle("")
        self.vectorMoveBox.setFlat(True)
        self.vectorMoveBox.setObjectName("vectorMoveBox")
        self.xPos = QtWidgets.QLineEdit(self.vectorMoveBox)
        self.xPos.setGeometry(QtCore.QRect(10, 10, 40, 30))
        self.xPos.setInputMethodHints(QtCore.Qt.ImhNone)
        self.xPos.setObjectName("xPos")
        self.yPos = QtWidgets.QLineEdit(self.vectorMoveBox)
        self.yPos.setGeometry(QtCore.QRect(60, 10, 40, 30))
        self.yPos.setInputMethodHints(QtCore.Qt.ImhNone)
        self.yPos.setObjectName("yPos")
        self.moveButton = QtWidgets.QPushButton(self.vectorMoveBox)
        self.moveButton.setGeometry(QtCore.QRect(0, 40, 113, 32))
        self.moveButton.setObjectName("moveButton")
        self.vectorMoveButton = QtWidgets.QPushButton(curveEditPanel)
        self.vectorMoveButton.setGeometry(QtCore.QRect(30, 140, 121, 32))
        self.vectorMoveButton.setObjectName("vectorMoveButton")
        self.scaleCurveButton = QtWidgets.QPushButton(curveEditPanel)
        self.scaleCurveButton.setGeometry(QtCore.QRect(30, 300, 121, 32))
        self.scaleCurveButton.setObjectName("scaleCurveButton")
        self.weightBox = QtWidgets.QGroupBox(curveEditPanel)
        self.weightBox.setGeometry(QtCore.QRect(30, 450, 101, 41))
        self.weightBox.setTitle("")
        self.weightBox.setFlat(True)
        self.weightBox.setObjectName("weightBox")
        self.weightVal = QtWidgets.QLineEdit(self.weightBox)
        self.weightVal.setGeometry(QtCore.QRect(60, 10, 40, 30))
        self.weightVal.setInputMethodHints(QtCore.Qt.ImhNone)
        self.weightVal.setObjectName("weightVal")
        self.weightLabel = QtWidgets.QLabel(self.weightBox)
        self.weightLabel.setGeometry(QtCore.QRect(10, 20, 60, 16))
        self.weightLabel.setObjectName("weightLabel")
        self.doneButton = QtWidgets.QPushButton(curveEditPanel)
        self.doneButton.setGeometry(QtCore.QRect(30, 610, 113, 32))
        self.doneButton.setObjectName("doneButton")
        self.reverseCurveButton = QtWidgets.QPushButton(curveEditPanel)
        self.reverseCurveButton.setGeometry(QtCore.QRect(30, 220, 121, 32))
        self.reverseCurveButton.setObjectName("reverseCurveButton")
        self.cancelButton = QtWidgets.QPushButton(curveEditPanel)
        self.cancelButton.setGeometry(QtCore.QRect(30, 580, 113, 32))
        self.cancelButton.setObjectName("cancelButton")
        self.joinSplitButton = QtWidgets.QPushButton(curveEditPanel)
        self.joinSplitButton.setGeometry(QtCore.QRect(30, 370, 121, 32))
        self.joinSplitButton.setObjectName("joinSplitButton")
        self.editWeightValBox = QtWidgets.QGroupBox(curveEditPanel)
        self.editWeightValBox.setGeometry(QtCore.QRect(30, 450, 101, 41))
        self.editWeightValBox.setTitle("")
        self.editWeightValBox.setFlat(True)
        self.editWeightValBox.setObjectName("editWeightValBox")
        self.editWeightVal = QtWidgets.QLineEdit(self.editWeightValBox)
        self.editWeightVal.setGeometry(QtCore.QRect(60, 10, 40, 30))
        self.editWeightVal.setInputMethodHints(QtCore.Qt.ImhNone)
        self.editWeightVal.setObjectName("editWeightVal")
        self.editWeightLabel = QtWidgets.QLabel(self.editWeightValBox)
        self.editWeightLabel.setGeometry(QtCore.QRect(10, 20, 60, 16))
        self.editWeightLabel.setObjectName("editWeightLabel")
        self.line = QtWidgets.QFrame(curveEditPanel)
        self.line.setGeometry(QtCore.QRect(-50, 530, 291, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(curveEditPanel)
        QtCore.QMetaObject.connectSlotsByName(curveEditPanel)

    def retranslateUi(self, curveEditPanel):
        _translate = QtCore.QCoreApplication.translate
        curveEditPanel.setWindowTitle(_translate("curveEditPanel", "Form"))
        self.rotateCurveButton.setText(_translate("curveEditPanel", "Rotate by angle"))
        self.scaleDoneButton.setText(_translate("curveEditPanel", "Done"))
        self.rotateDoneButton.setText(_translate("curveEditPanel", "Done"))
        self.addPointButton.setText(_translate("curveEditPanel", "Add point"))
        self.permutePointsButton.setText(_translate("curveEditPanel", "Permute points"))
        self.editWeightButton.setText(_translate("curveEditPanel", "Edit Weight"))
        self.undoButton.setText(_translate("curveEditPanel", "Undo"))
        self.exportCurveButton.setText(_translate("curveEditPanel", "Export"))
        self.deletePointButton.setText(_translate("curveEditPanel", "Delete point"))
        self.addButton.setText(_translate("curveEditPanel", "Add"))
        self.moveButton.setText(_translate("curveEditPanel", "Move"))
        self.vectorMoveButton.setText(_translate("curveEditPanel", "Move by vector"))
        self.scaleCurveButton.setText(_translate("curveEditPanel", "Scale"))
        self.weightLabel.setText(_translate("curveEditPanel", "weight:"))
        self.doneButton.setText(_translate("curveEditPanel", "Done"))
        self.reverseCurveButton.setText(_translate("curveEditPanel", "Reverse points"))
        self.cancelButton.setText(_translate("curveEditPanel", "Cancel"))
        self.joinSplitButton.setText(_translate("curveEditPanel", "Join / Split"))
        self.editWeightLabel.setText(_translate("curveEditPanel", "weight:"))
