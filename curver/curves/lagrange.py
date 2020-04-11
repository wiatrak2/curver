import numpy as np
from copy import deepcopy

from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import widgets
from curver.curves import Curve

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
        self.scene.addItem(new_point)
        self.points.append(new_point)
        if len(self.points) > 1:
            self._remove_segments()
            for i in range(len(self.points) - 1):
                segment = widgets.InterpolationCurve(self.points[i], self.points[i+1], self.interpolate)
                self.scene.addItem(segment)
                self.segments.append(segment)

    def manage_edit(self, allow=True):
        for point in self.points:
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemIsMovable, allow)
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemSendsGeometryChanges, allow)
            point.edit_mode = allow

    def extend_from_points(self, points: [QtCore.QPointF]):
        sorted_points = points
        sorted_points.sort(key = lambda p: p.x())
        self.points = [widgets.point.Point(p) for p in points]
        for p in self.points:
            self.scene.addItem(p)
        for i, point in enumerate(self.points[1:]):
            prev_point = self.points[i]
            curve_segment = widgets.interpolation_curve.InterpolationCurve(prev_point, point, self.interpolate)
            self.scene.addItem(curve_segment)
            self.segments.append(curve_segment)

    def delete_point(self, point: QtCore.QPointF):
        if point in self.points:
            points_copy = list(self.points)
            self.delete_curve()
            points_copy.remove(point)
            points = [p.point for p in points_copy]
            self.extend_from_points(points)

    def delete_curve(self):
        while len(self.points):
            point = self.points.pop()
            self.scene.removeItem(point)
        while len(self.segments):
            segment = self.segments.pop()
            self.scene.removeItem(segment)
