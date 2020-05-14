from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import CurveController
from curver.ui.curve_edit_list_ui import Ui_curveEditWindow


class CurvesListWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, curves={}):
        super().__init__(parent)

        assert parent.controller, "Parent of CurvesListWindow must have controller"
        self.controller: CurveController = parent.controller
        self._parent = parent
        self.curves = curves

        self.ui = Ui_curveEditWindow()
        self.ui.setupUi(self)
        self._set_actions()

    @property
    def selected_curve(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        return selected_curve_item.text()

    def closeEvent(self, e):
        self.controller.quit_expose_curve(self.selected_curve)
        for curve_id in self.curves:
            self.controller.hide_curve_details(curve_id)
        self._parent.edit_curve_list_close()
        return super().closeEvent(e)

    def show(self, *args, **kwargs):
        self.ui.curvesList.clear()
        self.ui.curvesList.addItems(self.curves)
        self.ui.curvesList.setCurrentRow(0)
        return super().show(*args, **kwargs)

    def change_visibility(self):
        self.controller.change_curve_visibility(self.selected_curve)

    def change_points_visibility(self):
        self.controller.change_curve_points_visibility(self.selected_curve)

    def edit(self):
        self._parent.edit_curve_start(self.selected_curve)

    def delete(self):
        self._parent.delete_curve(self.selected_curve)
        self.curves.remove(self.selected_curve)
        self.ui.curvesList.takeItem(self.ui.curvesList.currentRow())

    def done(self):
        self.close()

    def _curve_selection_change(self, current, previous):
        if previous is not None:
            previous_curve_id = previous.text()
            self.controller.quit_expose_curve(previous_curve_id)
        self.controller.expose_curve(self.selected_curve)

    def _set_actions(self):
        self.ui.changeCurveVisibilityButton.clicked.connect(self.change_visibility)
        self.ui.changePointsVisibilityButton.clicked.connect(
            self.change_points_visibility
        )
        self.ui.curveEditButton.clicked.connect(self.edit)
        self.ui.curveDeleteButton.clicked.connect(self.delete)
        self.ui.doneButton.clicked.connect(self.done)
        self.ui.curvesList.currentItemChanged.connect(self._curve_selection_change)
