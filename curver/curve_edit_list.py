from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver.curve_controller import CurveController
from curver.ui.curve_edit_list_ui import Ui_curveEditWindow


class CurvesListWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        assert parent.controller, "Parent of CurvesListWindow must have controller"
        self.controller: CurveController = parent.controller

        self.ui = Ui_curveEditWindow()
        self.ui.setupUi(self)
        self.curves = {}
        self._set_actions()

    def closeEvent(self, e):
        for curve_id in self.curves:
            self.controller.hide_curve_details(curve_id)
        self.parent().edit_curve_list_close()
        return super().closeEvent(e)

    def show(self, curves, *args, **kwargs):
        self.curves = curves
        self.ui.curvesList.clear()
        self.ui.curvesList.addItems(self.curves)
        self._setup_ui()
        return super().show(*args, **kwargs)

    def _setup_ui(self):
        for curve_id in self.curves:
            self.controller.show_curve(curve_id)

    def change_visibility(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        curve_id = selected_curve_item.text()
        self.controller.change_curve_visibility(curve_id)

    def change_points_visibility(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        curve_id = selected_curve_item.text()
        self.controller.change_curve_points_visibility(curve_id)

    def edit(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        curve_id = selected_curve_item.text()
        self.parent().edit_curve_start(curve_id)

    def delete(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        curve_id = selected_curve_item.text()
        self.ui.curvesList.takeItem(self.ui.curvesList.currentRow())
        self.parent().delete_curve(curve_id)

    def done(self):
        self.close()

    def _set_actions(self):
        self.ui.changeCurveVisibilityButton.clicked.connect(self.change_visibility)
        self.ui.changePointsVisibilityButton.clicked.connect(
            self.change_points_visibility
        )
        self.ui.curveEditButton.clicked.connect(self.edit)
        self.ui.curveDeleteButton.clicked.connect(self.delete)
        self.ui.doneButton.clicked.connect(self.done)
