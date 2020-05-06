import json
import logging
import numpy as np
from copy import deepcopy
from enum import Enum

import daiquiri
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import curves, utils, curve_controller, curve_join_window
from curver.ui.curve_edit_ui import Ui_curveEditWindow

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)


class CurveEditWindow(QtWidgets.QMainWindow):
    modes = utils.CurveModes

    def __init__(
        self,
        curve_id: str,
        parent=None,
        controller: curve_controller.CurveController = None,
    ):
        super().__init__(parent)
        self.curve_id = curve_id
        if controller is None:
            assert (
                parent.controller
            ), "parent of CurveEditWindow must have `controller` attribute"
            self.controller: curve_controller.CurveController = parent.controller
        else:
            self.controller: curve_controller.CurveController = controller

        self.ui = Ui_curveEditWindow()
        self.ui.setupUi(self)
        self.color_picker = QtWidgets.QColorDialog(parent=self)
        self._set_actions()

        self.mode = self.modes.NONE

        self._curve_join_window = None
        self._edited_point = None  # Used for points permutation

        self._setup_ui()

    def set_mode(self, new_mode):
        self.mode = new_mode
        self.controller.set_curve_mode(new_mode)
        self._update_ui()

    def _setup_ui(self):
        self.ui.curveName.setText(self.curve_id)
        utils.set_widget_geometry(self.color_picker, self, mode="left")
        self.color_picker.show()
        self._update_ui()

    def _update_ui(self):
        self.ui.addPointBox.setVisible(self.mode == self.modes.ADD_POINT)
        self.ui.vectorMoveBox.setVisible(self.mode == self.modes.MOVE_BY_VECTOR)
        self.ui.rotateCurveBox.setVisible(self.mode == self.modes.ROTATE_CURVE)
        self.ui.scaleCurveBox.setVisible(self.mode == self.modes.SCALE_CURVE)

    def _finish_edit(self):
        self.color_picker.close()
        if self._curve_join_window:
            self._curve_join_window.close()
        self.controller.rename_curve(self.curve_id, self.ui.curveName.text())
        self.parent().edit_curve_finish()

    def closeEvent(self, e):
        self._finish_edit()
        return super().closeEvent(e)

    def notify_scene_pos(self, point: QtCore.QPointF):
        x, y = point.x(), point.y()
        if self.mode == self.modes.ADD_POINT:
            self.ui.addXPos.setText(str(int(x)))
            self.ui.addYPos.setText(str(int(y)))

    def add_point_button(self):
        self.set_mode(self.modes.ADD_POINT)

    def add_point_final_button(self):
        if self.mode == self.modes.ADD_POINT:
            self._add_from_coordinates()

    def delete_point_button(self):
        self.set_mode(self.modes.DELETE_POINT)

    def move_by_vector_button(self):
        self.ui.vectorMoveBox.setHidden(False)
        self.set_mode(self.modes.MOVE_BY_VECTOR)

    def move_by_vector_final_button(self):
        if self.mode == self.modes.MOVE_BY_VECTOR:
            self._move_by_vector()

    def permute_points_button(self):
        self.set_mode(self.modes.PERMUTE_POINTS)

    def reverse_points_button(self):
        self.set_mode(self.modes.REVERSE_POINTS)
        return self._reverse_curve()

    def rotate_curve_button(self):
        self.set_mode(self.modes.ROTATE_CURVE)
        self.ui.rotationSlider.valueChanged.connect(self._rotate_curve_slider)
        self.ui.rotationSlider.setValue(0)

    def rotate_curve_final_button(self):
        self.ui.rotateCurveBox.setHidden(True)
        self.set_mode(self.modes.NONE)

    def scale_curve_button(self):
        self.set_mode(self.modes.SCALE_CURVE)
        self.ui.scaleSlider.valueChanged.connect(self._scale_curve_slider)
        self.ui.scaleSlider.setValue(50)

    def scale_curve_final_button(self):
        self.set_mode(self.modes.NONE)

    def export_curve_button(self):
        self.set_mode(self.modes.EXPORT_CURVE)
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save", "curve.json", ".json"
        )
        self._save_curve(filename[0])

    def join_button(self):
        self.set_mode(self.modes.JOIN_CURVE)
        curve_ids = self.controller.curve_ids()
        curve_ids.remove(self.curve_id)
        self._curve_join_window = curve_join_window.CurveJoinWindow(
            self.curve_id, curve_ids, parent=self
        )
        utils.set_widget_geometry(self._curve_join_window, self.parent(), "right")
        self._curve_join_window.show()

    def undo_button(self):
        self.controller.undo_curve_edit()

    def cancel_button(self):
        self.set_mode(self.modes.NONE)
        self.controller.edit_curve_cancel()
        self.close()

    def done_button(self):
        self.set_mode(self.modes.NONE)
        self.close()

    def _color_picker_action(self):
        color = self.color_picker.currentColor()
        self.controller.change_curve_color(color, self.curve_id)

    def _add_point(self, point: QtCore.QPointF):
        self.controller.add_point(point)
        self.set_mode(self.modes.NONE)

    def _add_from_coordinates(self):
        x, y = float(self.ui.addXPos.text()), float(self.ui.addYPos.text())
        point = QtCore.QPointF(x, y)
        self.controller.add_point(point)
        self.set_mode(self.modes.NONE)

    def _delete_point(self, point: QtCore.QPointF):
        self.controller.delete_point(point)
        self.set_mode(self.modes.NONE)

    def _move_by_vector(self):
        vec_x, vec_y = float(self.ui.xPos.text()), float(self.ui.yPos.text())
        vec_qt = QtCore.QPointF(vec_x, vec_y)
        self.controller.move_curve(vec_qt)
        self.set_mode(self.modes.NONE)

    def _permute_points(self, point: QtCore.QPointF):
        if self._edited_point is None:
            self._edited_point = point
            return
        self.controller.permute_points(self._edited_point, point)
        self._edited_point = None
        self.set_mode(self.modes.NONE)

    def _reverse_curve(self):
        self.controller.reverse_curve()
        self.set_mode(self.modes.NONE)

    def _rotate_curve_slider(self, curve_positions):
        angle = self.ui.rotationSlider.value() / self.ui.rotationSlider.maximum()
        self.controller.rotate_curve(angle)

    def _scale_curve_slider(self):
        SCALE_STEP = 0.1
        scale_factor = np.power(10, (self.ui.scaleSlider.value() * 2 / 100) - 1)
        self.controller.scale_curve(scale_factor)

    def _save_curve(self, filename):
        curve_dict = self.controller.serialize_curve()
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
        if self.mode == self.modes.JOIN_CURVE:
            if self._curve_join_window.mouse_click_action(point):
                self.close()

    def _set_actions(self):
        self.ui.addPointButton.clicked.connect(self.add_point_button)
        self.ui.addButton.clicked.connect(self.add_point_final_button)
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
        self.ui.joinWithCurveButton.clicked.connect(self.join_button)
        self.ui.undoButton.clicked.connect(self.undo_button)
        self.ui.cancelButton.clicked.connect(self.cancel_button)
        self.ui.doneButton.clicked.connect(self.done_button)
        self.color_picker.currentColorChanged.connect(self._color_picker_action)
