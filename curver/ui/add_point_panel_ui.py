# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curver/ui/add_point_panel.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addCurveWidget(object):
    def setupUi(self, addCurveWidget):
        addCurveWidget.setObjectName("addCurveWidget")
        addCurveWidget.resize(200, 650)
        self.addCurveButton = QtWidgets.QPushButton(addCurveWidget)
        self.addCurveButton.setGeometry(QtCore.QRect(30, 80, 140, 30))
        self.addCurveButton.setObjectName("addCurveButton")
        self.addPointBox = QtWidgets.QGroupBox(addCurveWidget)
        self.addPointBox.setEnabled(True)
        self.addPointBox.setGeometry(QtCore.QRect(0, 140, 180, 280))
        self.addPointBox.setTitle("")
        self.addPointBox.setFlat(True)
        self.addPointBox.setObjectName("addPointBox")
        self.xPos = QtWidgets.QLineEdit(self.addPointBox)
        self.xPos.setGeometry(QtCore.QRect(60, 60, 40, 30))
        self.xPos.setInputMethodHints(QtCore.Qt.ImhNone)
        self.xPos.setObjectName("xPos")
        self.yPos = QtWidgets.QLineEdit(self.addPointBox)
        self.yPos.setEnabled(True)
        self.yPos.setGeometry(QtCore.QRect(110, 60, 40, 30))
        self.yPos.setObjectName("yPos")
        self.addPointButton = QtWidgets.QPushButton(self.addPointBox)
        self.addPointButton.setGeometry(QtCore.QRect(30, 130, 140, 30))
        self.addPointButton.setObjectName("addPointButton")
        self.saveCurveButton = QtWidgets.QPushButton(self.addPointBox)
        self.saveCurveButton.setGeometry(QtCore.QRect(30, 250, 140, 30))
        self.saveCurveButton.setObjectName("saveCurveButton")
        self.curveName = QtWidgets.QLineEdit(self.addPointBox)
        self.curveName.setEnabled(True)
        self.curveName.setGeometry(QtCore.QRect(30, 20, 140, 30))
        self.curveName.setObjectName("curveName")
        self.undoAddPointButton = QtWidgets.QPushButton(self.addPointBox)
        self.undoAddPointButton.setGeometry(QtCore.QRect(30, 160, 140, 30))
        self.undoAddPointButton.setObjectName("undoAddPointButton")
        self.cancelAddCurveButton = QtWidgets.QPushButton(self.addPointBox)
        self.cancelAddCurveButton.setGeometry(QtCore.QRect(30, 220, 140, 30))
        self.cancelAddCurveButton.setObjectName("cancelAddCurveButton")
        self.weightBox = QtWidgets.QGroupBox(self.addPointBox)
        self.weightBox.setGeometry(QtCore.QRect(40, 100, 120, 30))
        self.weightBox.setAcceptDrops(False)
        self.weightBox.setAutoFillBackground(False)
        self.weightBox.setTitle("")
        self.weightBox.setFlat(True)
        self.weightBox.setObjectName("weightBox")
        self.weightVal = QtWidgets.QLineEdit(self.weightBox)
        self.weightVal.setGeometry(QtCore.QRect(70, 0, 40, 30))
        self.weightVal.setInputMethodHints(QtCore.Qt.ImhNone)
        self.weightVal.setObjectName("weightVal")
        self.weightLabel = QtWidgets.QLabel(self.weightBox)
        self.weightLabel.setGeometry(QtCore.QRect(10, 5, 60, 20))
        self.weightLabel.setObjectName("weightLabel")
        self.editCurveButton = QtWidgets.QPushButton(addCurveWidget)
        self.editCurveButton.setGeometry(QtCore.QRect(30, 500, 140, 30))
        self.editCurveButton.setObjectName("editCurveButton")
        self.setCurveType = QtWidgets.QComboBox(addCurveWidget)
        self.setCurveType.setGeometry(QtCore.QRect(30, 50, 140, 30))
        self.setCurveType.setObjectName("setCurveType")

        self.retranslateUi(addCurveWidget)
        QtCore.QMetaObject.connectSlotsByName(addCurveWidget)

    def retranslateUi(self, addCurveWidget):
        _translate = QtCore.QCoreApplication.translate
        addCurveWidget.setWindowTitle(_translate("addCurveWidget", "Form"))
        self.addCurveButton.setText(_translate("addCurveWidget", "Add Curve"))
        self.addPointButton.setText(_translate("addCurveWidget", "Add Point"))
        self.saveCurveButton.setText(_translate("addCurveWidget", "Done"))
        self.undoAddPointButton.setText(_translate("addCurveWidget", "Undo"))
        self.cancelAddCurveButton.setText(_translate("addCurveWidget", "Cancel"))
        self.weightVal.setPlaceholderText(_translate("addCurveWidget", "1.0"))
        self.weightLabel.setText(_translate("addCurveWidget", "weight:"))
        self.editCurveButton.setText(_translate("addCurveWidget", "Edit Curve"))
