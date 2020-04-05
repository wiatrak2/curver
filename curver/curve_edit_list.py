from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver.ui.curve_edit_list_ui import Ui_curveEditWindow

class CurvesListWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_curveEditWindow()
        self.ui.setupUi(self)
        self.curves = {}
        self._set_actions()

    def show(self, curves, *args, **kwargs):
        self.curves = curves
        self.ui.curvesList.clear()
        self.ui.curvesList.addItems(self.curves)
        return super().show(*args, **kwargs)

    def edit(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        curve_name = selected_curve_item.text()
        self.parent().manage_curve_edit(curve_name, allow=True)

    def delete(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        curve_name = selected_curve_item.text()
        self.ui.curvesList.takeItem(self.ui.curvesList.currentRow())
        self.parent().delete_curve(curve_name)

    def done(self):
        for curve_name in self.curves:
            self.parent().manage_curve_edit(curve_name, allow=False)
        self.close()

    def _set_actions(self):
        self.ui.curveEditButton.clicked.connect(self.edit)
        self.ui.curveDeleteButton.clicked.connect(self.delete)
        self.ui.doneButton.clicked.connect(self.done)
