from enum import Enum
from PyQt5 import uic, QtWidgets, QtGui, QtCore

import curves
import widgets
from ui.curve_edit_ui import Ui_curveEditWindow

class CurveEditWindow(QtWidgets.QMainWindow):
    class _Modes(Enum):
        NONE = 0
        ADD_POINT = 1
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

    def add_point(self, point: QtCore.QPointF):
        if self.mode == self.modes.ADD_POINT:
            self.curve.add_point(point)

    def _set_actions(self):
        self.ui.addPointButton.clicked.connect(self.add_point_button)
