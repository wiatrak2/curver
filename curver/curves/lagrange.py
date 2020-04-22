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
    def __init__(self, curve_name: str, scene: QtWidgets.QGraphicsScene):
        super().__init__(curve_name, scene)
        self.curve_name = curve_name
        self.scene = scene

        self.points: [widgets.point.Point] = []
        self.segments: [widgets.InterpolationCurve] = []

        self._rotation_angle = 0.
        self._scale_factor = 1.

    @property
    def _w(self):
        xs_all = np.array([p.x for p in self.points])
        xs = np.array([np.delete(xs_all, i) for i in range(len(xs_all))])
        denoms = xs_all[:, None] - xs
        return np.power(np.prod(denoms, axis=1), -1)

    def _remove_segments(self):
        while len(self.segments):
            segment = self.segments.pop()
            self.scene.removeItem(segment)

    def interpolate(self, x):
        xs = np.array([p.x for p in self.points])
        ys = np.array([p.y for p in self.points])
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
        self.delete_curve()
        points = [p.point for p in other.points]
        self.create_from_points(points)
        self.curve_name = other.curve_name

    def add_point(self, point: QtCore.QPointF):
        new_point = widgets.point.Point(point)
        new_point.add_segment(self)
        self.scene.addItem(new_point)
        self.points.append(new_point)
        if len(self.points) > 1:
            self._remove_segments()
            self._create_segments()

    def manage_edit(self, allow=True):
        for point in self.points:
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemIsMovable, allow)
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemSendsGeometryChanges, allow)
            point.edit_mode = allow

    def _create_segments(self):
        for i, point in enumerate(self.points[1:]):
            prev_point = self.points[i]
            curve_segment = widgets.interpolation_curve.InterpolationCurve(prev_point, point, self.interpolate)
            self.scene.addItem(curve_segment)
            self.segments.append(curve_segment)

    def create_from_points(self, points: [QtCore.QPointF]):
        sorted_points = points
        sorted_points.sort(key = lambda p: p.x())
        self.points = [widgets.point.Point(p) for p in points]
        logger.info(f"Creating curve from points: {self.points}.")
        for p in self.points:
            self.scene.addItem(p)
            p.add_segment(self)
        self._create_segments()

    def delete_point(self, point: QtCore.QPointF):
        if point in self.points:
            points_copy = list(self.points)
            self.delete_curve()
            points_copy.remove(point)
            points = [p.point for p in points_copy]
            self.create_from_points(points)

    def rotate_curve(self, angle: float, overwrite_angle=True, *args, **kwargs):
        if overwrite_angle:
            print(angle)
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
            self.scene.removeItem(point)
        while len(self.segments):
            segment = self.segments.pop()
            logger.info(f"Removing segment {segment}")
            self.scene.removeItem(segment)

    def notify_point_change(self, *args, **kwargs):
        self._remove_segments()
        self._create_segments()
