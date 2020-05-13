from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver.curve_controller import CurveController
from curver.ui.curve_join_ui import Ui_curveEditWindow


class CurveJoinWindow(QtWidgets.QMainWindow):
    def __init__(self, curve_id: str, curves: [str], parent: QtWidgets.QWidget = None):
        super().__init__(parent)

        assert parent.controller, "Parent of CurveJoinWindow must have controller"
        self.controller: CurveController = parent.controller
        self._parent = parent

        self.curve_id = curve_id
        self.curves = curves
        self._split_curve_mode = False

        self.ui = Ui_curveEditWindow()
        self.ui.setupUi(self)
        self._set_actions()

    @property
    def selected_curve(self):
        selected_curve_item = self.ui.curvesList.currentItem()
        return selected_curve_item.text()

    def closeEvent(self, e):
        self.controller.set_panel_widget(self._parent)
        return super().closeEvent(e)

    def show(self, *args, **kwargs):
        self.ui.curvesList.clear()
        self.ui.curvesList.addItems(self.curves)
        return super().show(*args, **kwargs)

    def _move_to_curve_button(self):
        self.controller.join_curves(self.curve_id, self.selected_curve)

    def _merge_button(self):
        self.controller.merge_curves(self.curve_id, self.selected_curve)

    def _split_curve_button(self):
        self._split_curve_mode = True

    def _done_button(self):
        self.close()

    def _split_curve(self, point: QtCore.QPointF):
        self.controller.split_curve(point, self.curve_id)

    def mouse_click_action(self, point: QtCore.QPointF) -> bool:
        """
        Return True if splitting curve succeed.
        """
        if self._split_curve_mode:
            self._split_curve(point)
            self._split_curve_mode = False
            return True
        return False

    def _set_actions(self):
        self.ui.moveToFirstButton.clicked.connect(self._move_to_curve_button)
        self.ui.mergeButton.clicked.connect(self._merge_button)
        self.ui.splitCurveButton.clicked.connect(self._split_curve_button)
        self.ui.doneButton.clicked.connect(self._done_button)
