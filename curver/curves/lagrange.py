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

    def set_state(self, other):
        self.delete_curve()
        points = [p.point for p in other.points]
        self.extend_from_points(points)
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

    def _create_from_points(self, points: [QtCore.QPointF]):
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
            self._create_from_points(points)

    def delete_curve(self):
        while len(self.points):
            point = self.points.pop()
            logger.info(f"Removing point {point}")
            self.scene.removeItem(point)
        while len(self.segments):
            segment = self.segments.pop()
            logger.info(f"Removing segment {segment}")
            self.scene.removeItem(segment)

    def _get_nearest_point(self, point: widgets.point.Point):
        nearest_point = None
        nearest_point_idx = None
        nearest_dist = 1e100
        for i, p in enumerate(self.points):
            dist_square = np.power(p.x - point.x, 2) + np.power(p.y - point.y, 2)
            if dist_square < nearest_dist:
                nearest_point = p
                nearest_point_idx = i
                nearest_dist = dist_square
        return nearest_point, nearest_point_idx

    def notify_point_change(self, old_point: widgets.point.Point, new_point: widgets.point.Point):
        #_, point_idx = self._get_nearest_point(old_point)
        #self.points[point_idx].point = new_point.point
        self._remove_segments()
        self._create_segments()
        return

        points = [p.point for p in self.points]
        points[point_idx] = new_point.point
        self.delete_curve()
        self._create_from_points(points)
        self.manage_edit()
        return


        _, point_idx = self._get_nearest_point(old_point)
        self.points[point_idx] = new_point
        points = [p.point for p in self.points]
        self.delete_curve()
        self.extend_from_points(points)