from copy import deepcopy

from PyQt5 import uic, QtWidgets, QtGui, QtCore

from widgets.point import Point
from widgets.line import Line

class Curve:
    def __init__(self, curve_name: str, scene: QtWidgets.QGraphicsScene):
        self.curve_name = curve_name
        self.scene = scene

        self.points = []
        self.drawn_points: [Point] = []
        self.drawn_segments: [Line] = []

    def add_point(self, point: QtCore.QPointF):
        raise NotImplementedError

    def remove_point(self, point: QtCore.QPointF):
        raise NotImplementedError

    def delete_curve(self):
        raise NotImplementedError

class Polyline(Curve):
    type = "Polyline"
    def __init__(self, curve_name: str, scene: QtWidgets.QGraphicsScene):
        super().__init__(curve_name, scene)

    def add_point(self, point: QtCore.QPointF):
        drawn_point = Point(point)
        self.scene.addItem(drawn_point)
        if len(self.points):
            last_drawn_point = self.drawn_points[-1]
            drawn_segment = Line(last_drawn_point, drawn_point)
            last_drawn_point.add_segment(drawn_segment)
            drawn_point.add_segment(drawn_segment)
            self.scene.addItem(drawn_segment)
            self.drawn_segments.append(drawn_segment)
        self.drawn_points.append(drawn_point)
        self.points.append(point)

    def manage_edit(self, allow=True):
        for point in self.drawn_points:
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemIsMovable, allow)
            point.edit_mode = allow

    def extend_from_points(self, points: [QtCore.QPointF]):
        for point in points:
            self.add_point(point)

    def remove_point(self, point: QtCore.QPointF):
        self.points.remove(point)
        points = deepcopy(self.points)
        self.delete_curve()
        self.extend_from_points(points)

    def delete_curve(self):
        while len(self.drawn_points):
            point = self.drawn_points.pop()
            self.scene.removeItem(point)
        while len(self.drawn_segments):
            segment = self.drawn_segments.pop()
            self.scene.removeItem(segment)
        self.points = []

