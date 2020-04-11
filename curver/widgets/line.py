import numpy as np
from copy import deepcopy

from PyQt5 import QtWidgets, QtGui, QtCore

from widgets.segment import Segment
from widgets.point import Point

class Line(Segment):
    def __init__(self, point_1: Point, point_2: Point, *args, **kwargs):
        self.point_1 = point_1
        self.point_2 = point_2
        self.segment = QtCore.QLineF(self.point_1.point, self.point_2.point)
        super().__init__(self.segment, *args, **kwargs)

    def __str__(self) -> str:
        return f"Line({self.point_1}, {self.point_2})"

    def __repr__(self) -> str:
        return str(self)

    def __deepcopy__(self, memo):
        new_line = Line(self.point_1, self.point_2)
        return new_line

    def _get_nearest_point(self, point: Point):
        nearest_point = None
        nearest_dist = 1e100
        for p in [self.point_1, self.point_2]:
            dist_square = np.power(p.x - point.x, 2) + np.power(p.y - point.y, 2)
            if dist_square < nearest_dist:
                nearest_point = p
                nearest_dist = dist_square
        return nearest_point

    def notify_point_change(self, old_point: Point, new_point: Point):
        point = self._get_nearest_point(old_point)
        if point == self.point_1:
            self.point_1 = new_point
            self.segment.setP1(self.point_1.point)
        else:
            self.point_2 = new_point
            self.segment.setP2(self.point_2.point)
        self.setLine(self.segment)


