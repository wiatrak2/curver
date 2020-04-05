import json
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
        SCALE_CURVE     = 7
        EXPORT_CURVE    = 8
    modes = _Modes

    def __init__(self, curve: curves.Curve, parent=None):
        super().__init__(parent)
        self.ui = Ui_curveEditWindow()
        self.ui.setupUi(self)
        self.curve = curve
        self._set_actions()

        self._edition_history = []
        self.mode = self.set_mode(self.modes.NONE)

        self._edited_point = None  # Used for points permutation
        self._initial_curve = deepcopy(self.curve)
        self._setup_ui()

    def set_mode(self, new_mode):
        if new_mode == self.modes.NONE:
            self._edition_history.append(deepcopy(self.curve))
        elif self.mode != self.modes.NONE:
            self.curve.set_state(self._edition_history[-1])
        self.mode = new_mode
        self._update_ui()

    def _setup_ui(self):
        self.ui.curveName.setText(self.curve.curve_name)
        self._update_ui()

    def _update_ui(self):
        self.ui.vectorMoveBox.setVisible(self.mode == self.modes.MOVE_BY_VECTOR)
        self.ui.rotateCurveBox.setVisible(self.mode == self.modes.ROTATE_CURVE)
        self.ui.scaleCurveBox.setVisible(self.mode == self.modes.SCALE_CURVE)

    def close(self, *args, **kwargs):
        self.curve.curve_name = self.ui.curveName.text()
        self.parent().finish_curve_edit()
        return super().close(*args, **kwargs)

    def add_point_button(self):
        self.set_mode(self.modes.ADD_POINT)

    def delete_point_button(self):
        self.set_mode(self.modes.DELETE_POINT)

    def move_by_vector_button(self):
        self.ui.vectorMoveBox.setHidden(False)
        self.set_mode(self.modes.MOVE_BY_VECTOR)

    def move_by_vector_final_button(self):
        if self.mode == self.modes.MOVE_BY_VECTOR:
            self._move_by_vector()
        self.ui.vectorMoveBox.setHidden(True)

    def permute_points_button(self):
        self.set_mode(self.modes.PERMUTE_POINTS)

    def reverse_points_button(self):
        self.set_mode(self.modes.REVERSE_POINTS)
        return self._reverse_curve()

    def rotate_curve_button(self):
        self.ui.rotateCurveBox.setHidden(False)
        self.ui.rotationSlider.valueChanged.connect(
            self._rotate_curve_slider(
                    [widgets.point.Point(p.point) for p in self.curve.points]
                )
            )
        self.ui.rotationSlider.setValue(0)
        self.set_mode(self.modes.ROTATE_CURVE)

    def rotate_curve_final_button(self):
        self.ui.rotateCurveBox.setHidden(True)
        self.set_mode(self.modes.NONE)

    def scale_curve_button(self):
        self.ui.scaleCurveBox.setHidden(False)
        self.ui.scaleSlider.valueChanged.connect(
            self._scale_curve_slider(
                    [widgets.point.Point(p.point) for p in self.curve.points]
                )
            )
        self.ui.scaleSlider.setValue(50)
        self.set_mode(self.modes.SCALE_CURVE)

    def scale_curve_final_button(self):
        self.ui.scaleCurveBox.setHidden(True)
        self.set_mode(self.modes.NONE)

    def export_curve_button(self):
        self.set_mode(self.modes.EXPORT_CURVE)
        filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save", "curve.json", ".json")
        self._save_curve(filename[0])

    def undo_button(self):
        if self.mode == self.modes.NONE:
            if len(self._edition_history) < 2:
                return
            _ = self._edition_history.pop()  # Current state
            previous_state = self._edition_history.pop()
            self.curve.set_state(previous_state)
        elif len(self._edition_history):
            previous_state = self._edition_history.pop()
            self.curve.set_state(previous_state)
        self.set_mode(self.modes.NONE)

        if len(self._edition_history):
            if self.mode == self.modes.NONE:
                last_state = self._edition_history.pop()
            self.curve.set_state(last_state)
        self.set_mode(self.modes.NONE)

    def cancel_button(self):
        self.set_mode(self.modes.NONE)
        self.curve.set_state(self._initial_curve)

    def done_button(self):
        self.set_mode(self.modes.NONE)
        self.close()

    def _add_point(self, point: QtCore.QPointF):
        self.curve.add_point(point)
        self.curve.manage_edit(allow=True)
        self.set_mode(self.modes.NONE)

    def _get_nearest_point(self, point: QtCore.QPointF):
        nearest_point = None
        nearest_dist = 1e100
        for p in self.curve.points:
            dist_square = np.power(p.x - point.x(), 2) + np.power(p.y - point.y(), 2)
            if dist_square < nearest_dist:
                nearest_point = p.point
                nearest_dist = dist_square
        return nearest_point

    def _delete_point(self, point: QtCore.QPointF):
        nearest_point = self._get_nearest_point(point)
        self.curve.delete_point(nearest_point)
        self.curve.manage_edit(allow=True)
        self.set_mode(self.modes.NONE)

    def _move_by_vector(self):
        vec_x, vec_y = float(self.ui.xPos.text()), float(self.ui.yPos.text())
        vec_qt = QtCore.QPointF(vec_x, vec_y)
        for point in self.curve.points:
            point.move_by_vector(vec_qt)
        self.set_mode(self.modes.NONE)

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
        self.set_mode(self.modes.NONE)

    def _reverse_curve(self):
        points = [p.point for p in self.curve.points[::-1]]
        self.curve.delete_curve()
        self.curve.extend_from_points(points)
        self.set_mode(self.modes.NONE)

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

    def _scale_curve_slider(self, curve_positions):
        SCALE_STEP = 0.1
        def _scale_curve():
            scale_factor = np.power(10, (self.ui.scaleSlider.value() * 2 / 100) - 1)
            for i, (point, position) in enumerate(zip(self.curve.points[1:], curve_positions[1:])):
                pos_vec_to_prev = position - curve_positions[i]
                scaled_vec = pos_vec_to_prev * scale_factor
                new_pos = self.curve.points[i] + scaled_vec
                point.set_scene_pos(new_pos.point)
        return _scale_curve

    def _save_curve(self, filename):
        curve_dict = {
            "curve_name": self.curve.curve_name,
            "points": [[p.x, p.y] for p in self.curve.points],
        }
        with open(filename, "w") as f:
            json.dump(curve_dict, f)
        self.set_mode(self.modes.NONE)

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
        self.ui.scaleCurveButton.clicked.connect(self.scale_curve_button)
        self.ui.scaleDoneButton.clicked.connect(self.scale_curve_final_button)
        self.ui.exportCurveButton.clicked.connect(self.export_curve_button)
        self.ui.undoButton.clicked.connect(self.undo_button)
        self.ui.cancelButton.clicked.connect(self.cancel_button)
        self.ui.doneButton.clicked.connect(self.done_button)
