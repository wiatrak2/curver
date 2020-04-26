import numpy as np
from copy import deepcopy

from PyQt5 import QtWidgets, QtGui, QtCore

from curver import widgets

class InterpolationCurve(widgets.GroupSegment):
    def __init__(self, point_1: widgets.Point, point_2: widgets.Point, interpolation, interval=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.point_1 = point_1
        self.point_2 = point_2
        self.interpolation = interpolation
        self.interval = interval
        self._segments = []
        self._construct_curve()

    def __deepcopy__(self, memo):
        new_curve = widgets.InterpolationCurve(self.point_1, self.point_2, self.interpolation, self.interval)
        return new_curve

    def _construct_curve(self):
        xs = np.arange(self.point_1.x, self.point_2.x, self.interval)[1:]
        if len(xs) and xs[-1] == self.point_2.x:
            xs = xs[:-1]
        ys = np.array(list(map(self.interpolation, xs)))
        points = [self.point_1] + [widgets.Point(QtCore.QPointF(x, y)) for x, y in zip(xs, ys)] + [self.point_2]
        for i in range(len(points) - 1):
            segment = widgets.Line(points[i], points[i+1])
            self.addToGroup(segment)
            self._segments.append(segment)

    def _get_nearest_point(self, point: widgets.Point):
        nearest_point = None
        nearest_dist = 1e100
        for p in [self.point_1, self.point_2]:
            dist_square = np.power(p.x - point.x, 2) + np.power(p.y - point.y, 2)
            if dist_square < nearest_dist:
                nearest_point = p
                nearest_dist = dist_square
        return nearest_point

    def notify_point_change(self, old_point: widgets.Point, new_point: widgets.Point):
        point = self._get_nearest_point(old_point)
        if point == self.point_1:
            self.point_1 = new_point
        else:
            self.point_2 = new_point
        for segment in self._segments:
            self.removeFromGroup(segment)

