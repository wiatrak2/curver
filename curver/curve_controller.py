import json
import logging
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Dict

import daiquiri
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from curver import curves, utils, widgets

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)


class CurveEntry:
    def __init__(self, curve: curves.Curve):
        self.curve = curve
        self.visible = True, True, True  # points, segments, details
        self.line_pen = QtGui.QPen(QtCore.Qt.black)
        self.points: [widgets.Point] = []
        self.segments: [widgets.Segment] = []
        self.details: [QtWidgets.QGraphicsItem] = []
        self.edition_history: [curves.Curve] = []


class CurveController:
    modes = utils.ControllerModes

    def __init__(self, scene: QtWidgets.QGraphicsScene):
        self.scene = scene

        self.curves: Dict[str, curves.Curve] = {}
        self.curve_entry: Dict[str, CurveEntry] = {}

        self._edited_curve = None

        self._initial_edited_curve = None

        self.mode = self.modes.NONE

    def _set_mode(self, mode):
        self.mode = mode
        if self.mode == self.modes.NONE:
            self.scene.notify_click = False
            self.scene.notify_position = False
        elif self.mode == self.modes.ADD or self.mode == self.modes.EDIT:
            self.scene.notify_click = True
            self.scene.notify_position = True

    def curve_ids(self) -> [str]:
        return list(self.curves.keys())

    def create_curve_start(self, curve_id: str, curve_cls: curves.Curve):
        self._set_mode(self.modes.ADD)
        self._edited_curve = curve_cls(curve_id)
        self.curves[curve_id] = self._edited_curve
        self.curve_entry[curve_id] = CurveEntry(self._edited_curve)

    def create_curve_finish(self):
        self.hide_curve_details()
        self._edited_curve = None
        self._set_mode(self.modes.NONE)

    def edit_curve_start(self, curve_id: str):
        self._set_mode(self.modes.EDIT)
        self._set_curve_points_moveability(curve_id, allow=True)
        self._edited_curve = self.curves[curve_id]
        self._initial_edited_curve = deepcopy(self._edited_curve)
        self.curve_entry[curve_id].edition_history = []
        self.show_curve(curve_id)

    def edit_curve_finish(self):
        if self._edited_curve:
            self._set_curve_points_moveability(self._edited_curve.id, allow=False)
            self._edited_curve = None
            self._initial_edited_curve = None
            self._set_mode(self.modes.NONE)

    def edit_curve_cancel(self):
        logger.info(f"Setting initial state = {self._initial_edited_curve.points}")
        self._edited_curve.set_state(self._initial_edited_curve)
        self._draw_curve(self._edited_curve)
        self._set_curve_points_moveability(self._edited_curve.id, allow=False)
        self._set_mode(self.modes.NONE)

    def set_curve_mode(self, mode, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        logger.info(f"Setting {curve.id} mode from {curve.mode} to {mode}")
        if curve.mode == curve.modes.NONE:
            self.curve_entry[curve.id].edition_history.append(deepcopy(curve))
        elif mode != curve.modes.NONE:
            self.undo_curve_edit(curve.id)
            self.curve_entry[curve.id].edition_history.append(deepcopy(curve))
        curve.set_mode(mode)

    def undo_curve_edit(self, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        curve_history = self.curve_entry[curve.id].edition_history
        if len(curve_history):
            curve_last_state = curve_history.pop()
            curve.set_state(curve_last_state)
            self._draw_curve(curve)

    def add_point(self, point: QtCore.QPointF, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        curve.add_point(point)
        logger.info(
            f"Curve {curve.id}: Added point {point}. All points: {curve.points}"
        )
        self._draw_curve(curve)

    def delete_point_idx(self, idx, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        try:
            curve.delete_point(curve.points[idx])
            self._draw_curve(curve)
        except IndexError:
            logger.info(
                f"Failed no remove point with index {idx} from curve with points {curve.points}."
            )

    def delete_point(self, point: QtCore.QPointF, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        rm_point = curve.get_nearest_point(point)
        curve.delete_point(rm_point)
        self._draw_curve(curve)

    def move_point(
        self, point: QtCore.QPointF, vector: QtCore.QPointF, curve_id: str = None
    ):
        curve = self.curves.get(curve_id, self._edited_curve)
        move_point = curve.get_nearest_point(point)
        curve.move_point(move_point, vector)

    def add_points(self, points: [QtCore.QPointF], curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        curve.add_points(points)
        self._draw_curve(curve)

    def permute_points(
        self, point_1: QtCore.QPointF, point_2: QtCore.QPointF, curve_id: str = None
    ):
        curve = self.curves.get(curve_id, self._edited_curve)
        p_1, p_2 = curve.get_nearest_point(point_1), curve.get_nearest_point(point_2)
        curve.permute_points(p_1, p_2)
        self._draw_curve(curve)

    def add_curve(
        self, curve_id: str, curve_cls: curves.Curve, curve_points: [QtCore.QPointF]
    ):
        curve = curve_cls(curve_id)
        curve.set_points(curve_points)
        self.curves[curve_id] = curve
        self.curve_entry[curve_id] = CurveEntry(curve)
        self._draw_curve(curve)

    def delete_curve(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.info(f"Deleting curve {curve_id}.")
        curve = self.curves.pop(curve_id)
        curve_entry = self.curve_entry.pop(curve_id)
        curve.delete_curve()
        for item in curve_entry.points + curve_entry.segments + curve_entry.details:
            self.scene.removeItem(item)

    def move_curve(self, vector: QtCore.QPointF, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        curve.move_curve(vector)
        self._draw_curve(curve)

    def reverse_curve(self, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        curve.reverse_curve()
        self._draw_curve(curve)

    def rotate_curve(self, angle_factor: float, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        curve.rotate_curve(angle_factor)
        self._draw_curve(curve)

    def scale_curve(self, scale_factor: float, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        curve.scale_curve(scale_factor)
        self._draw_curve(curve)

    def rename_curve(self, curve_id_old: str, curve_id_new: str = None):
        logger.info(f"Renaming curve. Arguments: {curve_id_old}, {curve_id_new}")
        if curve_id_new is None:
            curve_id_new = curve_id_old
            curve_id_old = self._edited_curve.id
        if curve_id_new in self.curves and curve_id_old != curve_id_new:
            logger.info("Failed to rename the curve.")
            return False
        if curve_id_old not in self.curves:
            logger.info(f"Curve {curve_id_old} not found.")
            return False
        curve = self.curves.pop(curve_id_old)
        curve_entry = self.curve_entry.pop(curve_id_old)
        curve.curve_id = curve_id_new
        self.curves[curve_id_new] = curve
        self.curve_entry[curve_id_new] = curve_entry
        return True

    def split_curve(self, point: QtCore.QPointF, curve_id: str = None):
        curve = self.curves.get(curve_id, self._edited_curve)
        split_point = curve.get_nearest_point(point)
        split_point_idx = curve.points.index(split_point)
        left_curve_id = f"{curve_id}_L"
        right_curve_id = f"{curve_id}_R"
        self.add_curve(left_curve_id, type(curve), curve.points[:split_point_idx])
        self.add_curve(right_curve_id, type(curve), curve.points[split_point_idx:])
        self._draw_curve(self.curves[left_curve_id])
        self._draw_curve(self.curves[right_curve_id])
        self.delete_curve(curve_id)
        self._edited_curve = None

    def join_curves(
        self,
        left_curve_id: str,
        right_curve_id: str,
        join_to_first_point=True,
    ):
        self.set_curve_mode(utils.CurveModes.MOVE_BY_VECTOR, left_curve_id)
        left_curve = self.curves[left_curve_id]
        right_curve = self.curves[right_curve_id]

        move_vec = (
            right_curve.points[0] - left_curve.points[0]
            if join_to_first_point
            else right_curve.points[-1] - left_curve.points[0]
        )
        self.move_curve(move_vec, left_curve)


    def merge_curves(self, left_curve_id: str, right_curve_id: str, join_to_first_point=True):
        self.set_curve_mode(utils.CurveModes.ADD_POINT, left_curve_id)
        left_curve = self.curves[left_curve_id]
        right_curve = self.curves[right_curve_id]
        self.add_points(right_curve.points, left_curve_id)
        self.delete_curve(right_curve_id)

    def show_curve(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.debug(f"Showing {curve_id}.")
        self.show_curve_points(curve_id)
        self.show_curve_segments(curve_id)
        self.show_curve_details(curve_id)

    def hide_curve(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.debug(f"Hiding {curve_id}.")
        self.hide_curve_points(curve_id)
        self.hide_curve_segments(curve_id)
        self.hide_curve_details(curve_id)

    def show_curve_points(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.debug(f"Showing {curve_id} points.")
        self._set_points_visibility(curve_id, True)

    def hide_curve_points(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.debug(f"Hiding {curve_id} points.")
        self._set_points_visibility(curve_id, False)

    def show_curve_segments(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.debug(f"Showing {curve_id} segments.")
        self._set_segments_visibility(curve_id, True)

    def hide_curve_segments(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.debug(f"Hiding {curve_id} segments.")
        self._set_segments_visibility(curve_id, False)

    def show_curve_details(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.debug(f"Showing {curve_id} details.")
        self._set_details_visibility(curve_id, True)

    def hide_curve_details(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.debug(f"Hiding {curve_id} details.")
        self._set_details_visibility(curve_id, False)

    def change_curve_visibility(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        curve_entry = self.curve_entry[curve_id]
        logger.info(
            f"Changing visibility of {curve_id}. Point/segmets/details visibility: {curve_entry.visible}"
        )
        if any(curve_entry.visible):
            self.hide_curve(curve_id)
        else:
            self.show_curve(curve_id)

    def change_curve_points_visibility(self, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        curve_entry = self.curve_entry[curve_id]
        logger.info(f"Changing visibility of {curve_id} points.")
        if curve_entry.visible[0]:
            self.hide_curve_points(curve_id)
        else:
            self.show_curve_points(curve_id)

    def _set_points_visibility(self, curve_id: str, make_visible=True):
        curve_entry = self.curve_entry[curve_id]
        for point in curve_entry.points:
            point.setVisible(make_visible)
        _, segments_visible, details_visible = curve_entry.visible
        self.curve_entry[curve_id].visible = (
            make_visible,
            segments_visible,
            details_visible,
        )

    def _set_segments_visibility(self, curve_id: str, make_visible=True):
        curve_entry = self.curve_entry[curve_id]
        for segment in curve_entry.segments:
            segment.setVisible(make_visible)
        points_visible, _, details_visible = curve_entry.visible
        self.curve_entry[curve_id].visible = (
            points_visible,
            make_visible,
            details_visible,
        )

    def _set_details_visibility(self, curve_id: str, make_visible=True):
        curve_entry = self.curve_entry[curve_id]
        for detail in curve_entry.details:
            detail.setVisible(make_visible)
        points_visible, segments_visible, _ = curve_entry.visible
        self.curve_entry[curve_id].visible = (
            points_visible,
            segments_visible,
            make_visible,
        )

    def change_curve_color(self, color: QtGui.QColor, curve_id: str = None):
        if curve_id is None:
            curve_id = self._edited_curve.id
        logger.debug(f"Changing {curve_id} color to {color.name()}.")
        curve_entry = self.curve_entry[curve_id]
        curve_entry.line_pen.setColor(color)
        self._draw_curve(curve_entry.curve)

    def serialize_curve(self, curve_id: str = None) -> dict:
        curve = self.curves.get(curve_id, self._edited_curve)
        return curve.serialize_curve()

    def _draw_curve(
        self,
        curve,
        draw_points=True,
        draw_details=True,
        points_pen: QtGui.QPen = None,
        segments_pen: QtGui.QPen = None,
        control_points_line_pen: QtGui.QPen = None,
    ):

        curve_entry = self.curve_entry[curve.id]
        if segments_pen is None:
            segments_pen = curve_entry.line_pen
        points, segments, details = curve.get_items(
            points_pen=points_pen,
            segments_pen=segments_pen,
            control_points_line_pen=control_points_line_pen,
        )

        curve_new_items = segments.copy()
        if draw_points:
            curve_new_items += points.copy()
        if draw_details:
            curve_new_items += details.copy()

        for item in curve_new_items:
            item.add_controller(self)
            self.scene.addItem(item)

        curve_points, curve_segments, curve_details = (
            curve_entry.points,
            curve_entry.segments,
            curve_entry.details,
        )
        curve_rm_items = curve_segments.copy()
        if draw_points:
            curve_rm_items += curve_points.copy()
        if draw_details:
            curve_rm_items += curve_details.copy()
        for item in curve_rm_items:
            self.scene.removeItem(item)

        curve_entry.segments = segments
        if draw_points:
            curve_entry.points = points
        if draw_details:
            curve_entry.details = details
        self._set_curve_points_moveability(curve.id, allow=self.mode == self.modes.EDIT)

    def _set_curve_points_moveability(self, curve_id: str, allow=True):
        curve = self.curves[curve_id]
        if curve.is_movable:
            curve_points = self.curve_entry[curve_id].points
            for point in curve_points:
                point.setFlag(QtWidgets.QGraphicsLineItem.ItemIsMovable, allow)
                point.edit_mode = allow

    # Point position change handling

    def notify_point_change(self, old_point, new_point):
        self._edited_curve.point_pos_change(old_point, new_point)
        self._draw_curve(self._edited_curve, draw_points=False)
