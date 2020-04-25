import json
import logging
from enum import Enum

import daiquiri
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import curves, widgets, utils
from curver.ui.main_ui import Ui_MainWindow
from curver.curve_edit_list import CurvesListWindow
from curver.curve_edit_window import CurveEditWindow
from copy import deepcopy

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)

class CurveEditor:
    class _Modes(Enum):
        NONE = 0
        ADD = 1
        EDIT = 2
    modes = _Modes

    def __init__(self, scene):
        self.scene = scene

        self.curves = {}
        self.curve_items = {}

        self.edited_curve = None
        self.mode = self.modes.NONE

    def _set_mode(self, mode):
        self.mode = mode
        if self.mode == self.modes.NONE:
            self.scene.notify_click = False
            self.scene.notify_position = False
        elif self.mode == self.modes.ADD or self.mode == self.modes.EDIT:
            self.scene.notify_click = True
            self.scene.notify_position = True

    def create_curve_start(self, curve_id: str, curve_cls: curves.Curve):
        self._set_mode(self.modes.ADD)
        self.edited_curve = curve_cls[curve_id]
        self.curves[curve_id] = self.edited_curve

    def create_curve_finish(self):
        self.edited_curve = None
        self.set_mode(self.modes.NONE)

    def edit_curve_start(self, curve_id):
        self._set_mode(self.modes.EDIT)
        self.edit_curve = self.curves[curve_id]

    def edit_curve_finish(self):
        self.edited_curve = None
        self.set_mode(self.modes.NONE)


    def add_point(self, curve_id: str, point: QtCore.QPointF):
        curve = self.curves[curve_id]
        curve.add_point(point)
        self._draw_curve(curve)

    def delete_point(self, curve_id: str, point: QtCore.QPointF):
        curve = self.curves[curve_id]
        curve.delete_point(point)
        self._draw_curve(curve)

    def delete_curve(self, curve_id: str):
        curve = self.curves.pop(curve_id)
        curve.delete_curve()

    def _draw_curve(self, curve, draw_points=True):
        points, segments = curve.get_items()
        items = points + segments if draw_points else segments
        for item in items:
            item.add_controller(self)
            self.scene.addItem(item)

        if curve.id in self.curve_items:
            curve_points, curve_segments = self.curve_items.pop(curve.id)
            curve_rm_items = curve_points + curve_segments if draw_points else curve_segments
            for item in curve_rm_items:
                self.scene.removeItem(item)
        self.curve_items[curve.id] = points, segments

    # Notifications from scene handling

    def notify_scene_pos(self, point: QtCore.QPointF):
        if self.mode == self.modes.NONE:
            return
        if self.mode == self.modes.ADD:
            return self._add_curve_scene_move_action(point)
        if self.mode == self.modes.EDIT:
            return self._edit_curve_scene_move_action(point)

    def notify_scene_click(self, point: QtCore.QPointF):
        if self.mode == self.modes.NONE:
            return
        if self.mode == self.modes.ADD:
            return self._add_curve_scene_click_action(point)
        if self.mode == self.modes.EDIT:
            return self._edit_curve_scene_click_action(point)

    # Point position change handling

    def notify_point_change(self, old_point, new_point):
        self.edited_curve.point_pos_change(old_point, new_point)
        self._draw_curve(self.edited_curve, draw_points=False)

