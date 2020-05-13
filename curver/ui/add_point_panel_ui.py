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
        addCurveWidget.resize(200, 620)
        self.mainPanelBox = QtWidgets.QGroupBox(addCurveWidget)
        self.mainPanelBox.setGeometry(QtCore.QRect(10, 10, 166, 580))
        self.mainPanelBox.setTitle("")
        self.mainPanelBox.setFlat(True)
        self.mainPanelBox.setObjectName("mainPanelBox")
        self.addPointBox = QtWidgets.QGroupBox(self.mainPanelBox)
        self.addPointBox.setEnabled(True)
        self.addPointBox.setGeometry(QtCore.QRect(20, 120, 131, 281))
        self.addPointBox.setTitle("")
        self.addPointBox.setFlat(True)
        self.addPointBox.setObjectName("addPointBox")
        self.xPos = QtWidgets.QLineEdit(self.addPointBox)
        self.xPos.setGeometry(QtCore.QRect(20, 60, 40, 30))
        self.xPos.setInputMethodHints(QtCore.Qt.ImhNone)
        self.xPos.setObjectName("xPos")
        self.yPos = QtWidgets.QLineEdit(self.addPointBox)
        self.yPos.setEnabled(True)
        self.yPos.setGeometry(QtCore.QRect(80, 60, 40, 30))
        self.yPos.setObjectName("yPos")
        self.addPointButton = QtWidgets.QPushButton(self.addPointBox)
        self.addPointButton.setGeometry(QtCore.QRect(10, 130, 113, 32))
        self.addPointButton.setObjectName("addPointButton")
        self.saveCurveButton = QtWidgets.QPushButton(self.addPointBox)
        self.saveCurveButton.setGeometry(QtCore.QRect(10, 250, 113, 32))
        self.saveCurveButton.setObjectName("saveCurveButton")
        self.curveName = QtWidgets.QLineEdit(self.addPointBox)
        self.curveName.setEnabled(True)
        self.curveName.setGeometry(QtCore.QRect(20, 20, 100, 30))
        self.curveName.setObjectName("curveName")
        self.undoAddPointButton = QtWidgets.QPushButton(self.addPointBox)
        self.undoAddPointButton.setGeometry(QtCore.QRect(10, 160, 113, 32))
        self.undoAddPointButton.setObjectName("undoAddPointButton")
        self.cancelAddCurveButton = QtWidgets.QPushButton(self.addPointBox)
        self.cancelAddCurveButton.setGeometry(QtCore.QRect(10, 220, 113, 32))
        self.cancelAddCurveButton.setObjectName("cancelAddCurveButton")
        self.weightBox = QtWidgets.QGroupBox(self.addPointBox)
        self.weightBox.setGeometry(QtCore.QRect(10, 100, 120, 30))
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
        self.weightLabel.setGeometry(QtCore.QRect(10, 5, 60, 16))
        self.weightLabel.setObjectName("weightLabel")
        self.addCurveButton = QtWidgets.QPushButton(self.mainPanelBox)
        self.addCurveButton.setGeometry(QtCore.QRect(40, 80, 113, 32))
        self.addCurveButton.setObjectName("addCurveButton")
        self.setCurveType = QtWidgets.QComboBox(self.mainPanelBox)
        self.setCurveType.setGeometry(QtCore.QRect(40, 50, 104, 26))
        self.setCurveType.setObjectName("setCurveType")
        self.editCurveButton = QtWidgets.QPushButton(self.mainPanelBox)
        self.editCurveButton.setGeometry(QtCore.QRect(30, 400, 113, 32))
        self.editCurveButton.setObjectName("editCurveButton")

        self.retranslateUi(addCurveWidget)
        QtCore.QMetaObject.connectSlotsByName(addCurveWidget)

    def retranslateUi(self, addCurveWidget):
        _translate = QtCore.QCoreApplication.translate
        addCurveWidget.setWindowTitle(_translate("addCurveWidget", "Form"))
        self.addPointButton.setText(_translate("addCurveWidget", "Add Point"))
        self.saveCurveButton.setText(_translate("addCurveWidget", "Done"))
        self.undoAddPointButton.setText(_translate("addCurveWidget", "Undo"))
        self.cancelAddCurveButton.setText(_translate("addCurveWidget", "Cancel"))
        self.weightVal.setPlaceholderText(_translate("addCurveWidget", "1.0"))
        self.weightLabel.setText(_translate("addCurveWidget", "weight:"))
        self.addCurveButton.setText(_translate("addCurveWidget", "Add Curve"))
        self.editCurveButton.setText(_translate("addCurveWidget", "Edit Curve"))
