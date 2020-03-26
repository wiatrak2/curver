from copy import deepcopy

from PyQt5 import uic, QtWidgets, QtGui, QtCore

from widgets.point import Point
from widgets.line import Line

class Curve:
    def __init__(self, curve_name):
        self.curve_name = curve_name
        self.points = []

        self.drawn_points: [Point] = []
        self.drawn_segments: [Line] = []

    def set_name(self, name: str):
        self.name = name

    def add_point(self, point: QtCore.QPointF, scene: QtWidgets.QGraphicsScene):
        raise NotImplementedError

    def remove_point(self, point: QtCore.QPointF, scene: QtWidgets.QGraphicsScene):
        raise NotImplementedError

    def delete_curve(self, scene: QtWidgets.QGraphicsScene):
        raise NotImplementedError

class Polyline(Curve):
    type = "Polyline"
    def __init__(self, curve_name):
        super().__init__(curve_name)

        self.segmentPen = QtGui.QPen(QtCore.Qt.black)

    def add_point(self, point: QtCore.QPointF, scene: QtWidgets.QGraphicsScene):
        drawn_point = Point(point)
        scene.addItem(drawn_point)
        if len(self.points):
            last_point, last_drawn_point = self.points[-1], self.drawn_points[-1]
            drawn_segment = Line(last_point, point)
            last_drawn_point.add_segment(drawn_segment)
            drawn_point.add_segment(drawn_segment)
            scene.addItem(drawn_segment)
            self.drawn_segments.append(drawn_segment)
        self.drawn_points.append(drawn_point)
        self.points.append(point)

    def manage_edit(self, allow=True):
        for point in self.drawn_points:
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemIsMovable, allow)
            point.edit_mode = allow

    def extend_from_points(self, points: [QtCore.QPointF], scene: QtWidgets.QGraphicsScene):
        for point in points:
            self.add_point(point, scene)

    def remove_point(self, point: QtCore.QPointF, scene: QtWidgets.QGraphicsScene):
        self.points.remove(point)
        points = deepcopy(self.points)
        self.delete_curve(scene)
        self.extend_from_points(points, scene)

    def delete_curve(self, scene: QtWidgets.QGraphicsScene):
        while len(self.drawn_points):
            point = self.drawn_points.pop()
            scene.removeItem(point)
        while len(self.drawn_segments):
            segment = self.drawn_segments.pop()
            scene.removeItem(segment)
        self.points = []

