from PyQt5 import uic, QtWidgets, QtGui, QtCore

from ui.curve_edit_ui import Ui_curveEditWindow

class CurveEditWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_curveEditWindow()
        self.ui.setupUi(self)
        self.curves = {}
        self._set_actions()

    def show(self, curves, *args, **kwargs):
        print(curves)
        self.curves = curves
        self.ui.curvesList.clear()
        self.ui.curvesList.addItems(self.curves)
        return super().show(*args, **kwargs)

    def edit(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        curve_id = selected_curve_item.text()
        curve = self.curves[curve_id]
        print(curve)

    def delete(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        curve_id = selected_curve_item.text()
        self.ui.curvesList.takeItem(self.ui.curvesList.currentRow())
        self.parent().delete_curve(curve_id)

    def _set_actions(self):
        self.ui.curveEditButton.clicked.connect(self.edit)
        self.ui.curveDeleteButton.clicked.connect(self.delete)
