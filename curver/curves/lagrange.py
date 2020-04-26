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
    def _w(self):
        xs_all = np.array([p.x() for p in self.points])
        xs = np.array([np.delete(xs_all, i) for i in range(len(xs_all))])
        denoms = xs_all[:, None] - xs
        return np.power(np.prod(denoms, axis=1), -1)

    def interpolate(self, x):
        xs = np.array([p.x() for p in self.points])
        ys = np.array([p.y() for p in self.points])
        enom = np.sum(self._w * ys / (x - xs))
        denom = np.sum(self._w / (x - xs))
        return enom / denom

    def set_mode(self, mode):
        if mode == self.modes.NONE and self.mode != self.modes.NONE:
            self.rotate_curve(self._rotation_angle, overwrite_angle=False)
            self.scale_curve(self._scale_factor, overwrite_factor=False)
        elif mode != self.modes.NONE:
            self.rotate_curve(0, overwrite_angle=False)
            self.scale_curve(1, overwrite_factor=False)
        self.mode = mode

    def set_state(self, other):
        self.points = other.points
        self.curve_id = other.curve_id

    def add_point(self, point: QtCore.QPointF):
        self.points.append(point)

    def _create_segments(self):
        for i, point in enumerate(self.points[1:]):
            prev_point = self.points[i]
            curve_segment = widgets.interpolation_curve.InterpolationCurve(prev_point, point, self.interpolate)
            self.segments.append(curve_segment)

    def _create_from_points(self, points: [QtCore.QPointF]):
        sorted_points = points
        sorted_points.sort(key = lambda p: p.x())
        self.points = [widgets.point.Point(p) for p in points]
        logger.info(f"Creating curve from points: {self.points}.")
        for p in self.points:
            p.add_segment(self)
        self._create_segments()

    def delete_point(self, point: QtCore.QPointF):
        if point in self.points:
            self.points.remove(point)

    def rotate_curve(self, angle: float, overwrite_angle=True, *args, **kwargs):
        if overwrite_angle:
            self._rotation_angle = angle
        angle = 360 * angle
        for item in self.segments + self.points:
            item.setTransformOriginPoint(self.points[0].point)
            item.setRotation(angle)

    def scale_curve(self, scale_factor: float, overwrite_factor=True, *args, **kwargs):
        if overwrite_factor:
            self._scale_factor = scale_factor
        for item in self.segments + self.points:
            item.setTransformOriginPoint(self.points[0].point)
            item.setScale(scale_factor)

    def delete_curve(self):
        while len(self.points):
            point = self.points.pop()
            logger.info(f"Removing point {point}")

    def get_items(self):
        points = [widgets.point.Point(p) for p in self.points]
        segments = []
        for i, point in enumerate(points[1:]):
            prev_point = points[i]
            curve_segment = widgets.interpolation_curve.InterpolationCurve(prev_point, point, self.interpolate)
            segments.append(curve_segment)
        return points, segments
