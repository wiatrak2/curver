import math
import logging
import numpy as np
from copy import deepcopy
from enum import Enum

from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import curves, widgets
from curver.ui.curve_edit_ui import Ui_curveEditWindow

logger = logging.getLogger(__name__)

class CurveEditWindow(QtWidgets.QMainWindow):
    class _Modes(Enum):
        NONE            = 0
        ADD_POINT       = 1
        DELETE_POINT    = 2
        MOVE_BY_VECTOR  = 3
        PERMUTE_POINTS  = 4
        REVERSE_POINTS  = 5
        ROTATE_CURVE    = 6
    modes = _Modes

    def __init__(self, curve: curves.Curve, parent=None):
        super().__init__(parent)
        self.ui = Ui_curveEditWindow()
        self.ui.setupUi(self)
        self.curve = curve
        self._set_actions()
        self._setup_ui()

        self.mode = self.modes.NONE

        self._edited_point = None  # Used for points permutation

    def _setup_ui(self):
        self.ui.vectorMoveBox.setHidden(True)
        self.ui.rotateCurveBox.setHidden(True)
        self.ui.scaleCurveBox.setHidden(True)

    def add_point_button(self):
        self.mode = self.modes.ADD_POINT

    def delete_point_button(self):
        self.mode = self.modes.DELETE_POINT

    def move_by_vector_button(self):
        self.ui.vectorMoveBox.setHidden(False)
        self.mode = self.modes.MOVE_BY_VECTOR

    def move_by_vector_final_button(self):
        if self.mode == self.modes.MOVE_BY_VECTOR:
            self._move_by_vector()
        self.ui.vectorMoveBox.setHidden(True)

    def permute_points_button(self):
        self.mode = self.modes.PERMUTE_POINTS

    def reverse_points_button(self):
        self.mode = self.modes.REVERSE_POINTS
        return self._reverse_curve()

    def rotate_curve_button(self):
        self.ui.rotateCurveBox.setHidden(False)
        self.ui.rotationSlider.valueChanged.connect(
            self._rotate_curve_slider(
                    [widgets.point.Point(p.point) for p in self.curve.points]
                )
            )
        self.ui.rotationSlider.setValue(0)
        self.mode = self.modes.ROTATE_CURVE

    def rotate_curve_final_button(self):
        self.ui.rotateCurveBox.setHidden(True)
        self.mode = self.modes.NONE

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
                nearest_point = p.point
                nearest_dist = dist_square
        return nearest_point

    def _delete_point(self, point: QtCore.QPointF):
        nearest_point = self._get_nearest_point(point)
        self.curve.delete_point(nearest_point)
        self.curve.manage_edit(allow=True)
        self.mode = self.modes.NONE

    def _move_by_vector(self):
        vec_x, vec_y = float(self.ui.xPos.text()), float(self.ui.yPos.text())
        vec_qt = QtCore.QPointF(vec_x, vec_y)
        for point in self.curve.points:
            point.move_by_vector(vec_qt)
        self.mode = self.modes.NONE

    def _permute_points(self, point: QtCore.QPointF):
        nearest_point: QtCore.QPointF = self._get_nearest_point(point)
        if self._edited_point is None:
            self._edited_point = nearest_point
            return
        try:
            p_1_idx, p_2_idx = self.curve.points.index(nearest_point), self.curve.points.index(self._edited_point)
            self.curve.points[p_1_idx].set_scene_pos(self._edited_point)
            self.curve.points[p_2_idx].set_scene_pos(nearest_point)
        except ValueError as e:
            logger.warning(f"Failure while permuting points: {self._edited_point} and {nearest_point}. Expetion: {e}")
        self._edited_point = None
        self.mode = self.modes.NONE

    def _reverse_curve(self):
        points = [p.point for p in self.curve.points[::-1]]
        self.curve.delete_curve()
        self.curve.extend_from_points(points)
        self.mode = self.modes.NONE

    def _rotate_curve_slider(self, curve_positions):
        def _rotate_curve():
            angle = (2 * np.pi) * self.ui.rotationSlider.value() / self.ui.rotationSlider.maximum()
            point_rotate_about = self.curve.points[0]  # TODO: allow rotation over other point
            for (point, position) in zip(self.curve.points, curve_positions):
                point_relative_pos = position - point_rotate_about
                new_x = round(point_relative_pos.x * np.cos(angle) - point_relative_pos.y * np.sin(angle), 2)
                new_y = round(point_relative_pos.x * np.sin(angle) + point_relative_pos.y * np.cos(angle), 2)
                point.set_scene_pos(QtCore.QPointF(new_x, new_y) + point_rotate_about.point)
        return _rotate_curve

    def mouse_click_action(self, point: QtCore.QPointF):
        if self.mode == self.modes.ADD_POINT:
            return self._add_point(point)
        if self.mode == self.modes.DELETE_POINT:
            return self._delete_point(point)
        if self.mode == self.modes.MOVE_BY_VECTOR:
            return
        if self.mode == self.modes.PERMUTE_POINTS:
            return self._permute_points(point)
        if self.mode == self.modes.REVERSE_POINTS:
            return
        if self.mode == self.modes.ROTATE_CURVE:
            return

    def _set_actions(self):
        self.ui.addPointButton.clicked.connect(self.add_point_button)
        self.ui.deletePointButton.clicked.connect(self.delete_point_button)
        self.ui.vectorMoveButton.clicked.connect(self.move_by_vector_button)
        self.ui.moveButton.clicked.connect(self.move_by_vector_final_button)
        self.ui.permutePointsButton.clicked.connect(self.permute_points_button)
        self.ui.reverseCurveButton.clicked.connect(self.reverse_points_button)
        self.ui.rotateCurveButton.clicked.connect(self.rotate_curve_button)
        self.ui.rotateDoneButton.clicked.connect(self.rotate_curve_final_button)
