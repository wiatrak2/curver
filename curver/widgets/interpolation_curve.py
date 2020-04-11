import numpy as np
from copy import deepcopy

from PyQt5 import QtWidgets, QtGui, QtCore

from widgets.group_segment import GroupSegment
from widgets.line import Line
from widgets.point import Point

class InterpolationCurve(GroupSegment):
    def __init__(self, point_1: Point, point_2: Point, interpolation, interval: float = 1, *args, **kwargs):
        self.point_1 = point_1
        self.point_2 = point_2
        self.interpolation = interpolation
        self.interval = interval
        super().__init__(*args, **kwargs)
        self._construct_curve()

    def __deepcopy__(self, memo):
        raise NotImplementedError

    def _construct_curve(self):
        xs = np.arange(self.point_1.x, self.point_2.x, self.interval)[1:]
        if xs[-1] == self.point_2.x:
            xs = xs[:-1]
        ys = np.array(list(map(self.interpolation, xs)))
        points = [self.point_1] + [Point(QtCore.QPointF(x, y)) for x, y in zip(xs, ys)] + [self.point_2]
        for i in range(len(points) - 1):
            self.addToGroup(Line(points[i], points[i+1]))
