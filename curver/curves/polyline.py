import logging
from copy import deepcopy

import daiquiri
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import widgets
from curver.curves import Curve
import numpy as np

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)

class Polyline(Curve):
    type = "Polyline"
    def __init__(self, curve_name: str):
        super().__init__(curve_name)
        self._edition_relative_position: [QtCore.QPointF] = None

    def set_mode(self, mode):
        logger.info(f"Setting mode {mode}.")
        self.mode = mode
        if mode == self.modes.ROTATE_CURVE or mode == self.modes.SCALE_CURVE:
            self._edition_relative_position = deepcopy(self.points)

    def set_state(self, other):
        self.delete_curve()
        points = [p.point for p in other.points]
        self.set_points(points)
        self.curve_name = other.curve_name

    def set_points(self, points: [QtCore.QPointF]):
        self.points = points

    def add_point(self, point: QtCore.QPointF):
        self.points.append(point)
        logger.info(f"Added point {point}. All points: {self.points}")
        return

        new_point = widgets.point.Point(point)
        if len(self.points):
            last_point = self.points[-1]
            new_segment = widgets.line.Line(last_point, new_point)
            last_point.add_segment(new_segment)
            new_point.add_segment(new_segment)
            self.segments.append(new_segment)
        self.points.append(new_point)

    def manage_edit(self, allow=True):
        return
        for point in self.points:
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemIsMovable, allow)
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemSendsGeometryChanges, allow)
            point.edit_mode = allow

    def delete_point(self, point: QtCore.QPointF):
        if point in self.points:
            self.points.remove(point)

    def move_point(self, point: QtCore.QPointF, vector: QtCore.QPointF):
        if point in self.points:
            self.points[self.points.index(point)] += vector

    def permute_points(self, point_1: QtCore.QPointF, point_2: QtCore.QPointF):
        if point_1 in self.points and point_2 in self.points:
            p_1_idx, p_2_idx = self.points.index(point_1), self.points.index(point_2)
            self.points[p_1_idx], self.points[p_2_idx] = self.points[p_2_idx], self.points[p_1_idx]

    def move_curve(self, vector: QtCore.QPointF, *args, **kwargs):
        for point in self.points:
            point += vector

    def reverse_curve(self, *args, **kwargs):
        self.points = self.points[::-1]

    def rotate_curve(self, angle_factor: float):
        angle = (2 * np.pi) * angle_factor
        point_rotate_about = self.points[0]  # TODO: allow rotation over other point
        for i, (point, position) in enumerate(zip(self.points, self._edition_relative_position)):
            point_relative_pos = position - point_rotate_about
            new_x = round(point_relative_pos.x() * np.cos(angle) - point_relative_pos.y() * np.sin(angle), 2)
            new_y = round(point_relative_pos.x() * np.sin(angle) + point_relative_pos.y() * np.cos(angle), 2)
            self.points[i] = QtCore.QPointF(new_x, new_y) + point_rotate_about

    def scale_curve(self, scale_factor: float):
        for i, position in enumerate(self._edition_relative_position[1:]):
           pos_vec_to_prev = position - self._edition_relative_position[i]
           scaled_vec = pos_vec_to_prev * scale_factor
           self.points[i+1] = self.points[i] + scaled_vec

    def delete_curve(self):
        self.points = []

    def get_nearest_point(self, point: QtCore.QPointF):
        nearest_point = None
        nearest_dist = 1e100
        for p in self.points:
            dist_square = np.power(p.x() - point.x(), 2) + np.power(p.y() - point.y(), 2)
            if dist_square < nearest_dist:
                nearest_point = p
                nearest_dist = dist_square
        return nearest_point

    def point_pos_change(self, old_point: widgets.point.Point, new_point: widgets.point.Point):
        point = self.get_nearest_point(old_point.point)
        self.points[self.points.index(point)] = new_point.point

    def get_items(self) -> [QtWidgets.QGraphicsItem]:
        points = [widgets.point.Point(p) for p in self.points]
        lines = [widgets.line.Line(points[i], points[i+1]) for i in range(len(points)-1)]
        return points, lines