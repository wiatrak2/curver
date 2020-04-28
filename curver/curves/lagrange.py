import logging
import numpy as np
from copy import deepcopy

import daiquiri
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import widgets
from curver.curves import Curve

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)

class Lagrange(Curve):
    type = "Lagrange"
    def __init__(self, curve_id: str):
        super().__init__(curve_id)

        self._rotation_angle = 0.
        self._scale_factor = 1.

    @property
    def is_movable(self):
        return self._rotation_angle == 0 and self._scale_factor == 1

    @property
    def _w(self):
        xs_all = np.array([p.x() for p in self.points])
        xs = np.array([np.delete(xs_all, i) for i in range(len(xs_all))])
        denoms = xs_all[:, None] - xs
        return np.power(np.prod(denoms, axis=1), -1)

    def _make_moveable(self):
        self._rotation_angle = 0.
        self._scale_factor = 1.

    def set_mode(self, mode):
        self.mode = mode

    def set_state(self, other):
        self.points = other.points
        self.curve_id = other.curve_id

    def set_points(self, points: [QtCore.QPointF]):
        points.sort(key = lambda p: p.x())
        self.points = points

    def add_point(self, point: QtCore.QPointF):
        if self.is_movable:
            self.points.append(point)
            self.points.sort(key = lambda p: p.x())
        else:
            self._make_moveable()

    def delete_point(self, point: QtCore.QPointF):
        if self.is_movable:
            if point in self.points:
                self.points.remove(point)
        else:
            self._make_moveable()

    def move_point(self, point: QtCore.QPointF, vector: QtCore.QPointF):
        if point in self.points:
            self.points[self.points.index(point)] += vector

    def permute_points(self, point_1: QtCore.QPointF, point_2: QtCore.QPointF):
        pass

    def move_curve(self, vector: QtCore.QPointF, *args, **kwargs):
        for point in self.points:
            point += vector

    def reverse_curve(self, *args, **kwargs):
        pass

    def rotate_curve(self, angle_factor: float, *args, **kwargs):
        self._rotation_angle = angle_factor

    def scale_curve(self, scale_factor: float, *args, **kwargs):
        self._scale_factor = scale_factor

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
        self.points.sort(key = lambda p: p.x())

    def _interpolate(self, x, *args, **kwargs):
        xs = np.array([p.x() for p in self.points])
        ys = np.array([p.y() for p in self.points])
        enom = np.sum(self._w * ys / (x - xs))
        denom = np.sum(self._w / (x - xs))
        return QtCore.QPointF(x, enom / denom)

    def get_items(self):
        points = [widgets.point.Point(p) for p in self.points]
        segments = []
        for i, point in enumerate(points[1:]):
            prev_point = points[i]
            curve_segment = widgets.interpolation_curve.InterpolationCurve(prev_point, point, self._interpolate)
            segments.append(curve_segment)

            angle = 360 * self._rotation_angle
            point.setTransformOriginPoint(self.points[0])
            point.setRotation(angle)
            point.setScale(self._scale_factor)
            curve_segment.setTransformOriginPoint(self.points[0])
            curve_segment.setRotation(angle)
            curve_segment.setScale(self._scale_factor)

        return points, segments
