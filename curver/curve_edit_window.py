import math
from enum import Enum

from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import curves, widgets
from curver.ui.curve_edit_ui import Ui_curveEditWindow

class CurveEditWindow(QtWidgets.QMainWindow):
    class _Modes(Enum):
        NONE            = 0
        ADD_POINT       = 1
        DELETE_POINT    = 2
    modes = _Modes
    def __init__(self, curve: curves.Curve, parent=None):
        super().__init__(parent)
        self.ui = Ui_curveEditWindow()
        self.ui.setupUi(self)
        self.curve = curve
        self._set_actions()
        self.mode = self.modes.NONE

    def add_point_button(self):
        self.mode = self.modes.ADD_POINT

    def delete_point_button(self):
        self.mode = self.modes.DELETE_POINT

    def _add_point(self, point: QtCore.QPointF):
        self.curve.add_point(point)
        self.curve.manage_edit(allow=True)
        self.mode = self.modes.NONE

    def _get_nearest_point(self, point: QtCore.QPointF):
        nearest_point = None
        nearest_dist = 1e100
        for p in self.curve.points:
            dist_square = math.pow(p.x - point.x(), 2) + math.pow(p.y - point.y(), 2)
            if dist_square < nearest_dist:
                nearest_point = p
                nearest_dist = dist_square
        return nearest_point

    def _delete_point(self, point: QtCore.QPointF):
        nearest_point = self._get_nearest_point(point)
        self.curve.delete_point(nearest_point)
        self.curve.manage_edit(allow=True)
        self.mode = self.modes.NONE

    def mouse_click_action(self, point: QtCore.QPointF):
        if self.mode == self.modes.ADD_POINT:
            return self._add_point(point)
        if self.mode == self.modes.DELETE_POINT:
            return self._delete_point(point)

    def _set_actions(self):
        self.ui.addPointButton.clicked.connect(self.add_point_button)
        self.ui.deletePointButton.clicked.connect(self.delete_point_button)
