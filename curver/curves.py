from copy import deepcopy

from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import widgets

class Curve:
    def __init__(self, curve_name: str, scene: QtWidgets.QGraphicsScene):
        self.curve_name = curve_name
        self.scene = scene

        self.points: [widgets.point.Point] = []
        self.segments: [widgets.line.Line] = []

    def add_point(self, point: QtCore.QPointF):
        raise NotImplementedError

    def delete_point(self, point: QtCore.QPointF):
        raise NotImplementedError

    def delete_curve(self):
        raise NotImplementedError

class Polyline(Curve):
    type = "Polyline"
    def __init__(self, curve_name: str, scene: QtWidgets.QGraphicsScene):
        super().__init__(curve_name, scene)

    def add_point(self, point: QtCore.QPointF):
        new_point = widgets.point.Point(point)
        self.scene.addItem(new_point)
        if len(self.points):
            last_point = self.points[-1]
            new_segment = widgets.line.Line(last_point, new_point)
            last_point.add_segment(new_segment)
            new_point.add_segment(new_segment)
            self.scene.addItem(new_segment)
            self.segments.append(new_segment)
        self.points.append(new_point)

    def manage_edit(self, allow=True):
        for point in self.points:
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemIsMovable, allow)
            point.setFlag(QtWidgets.QGraphicsLineItem.ItemSendsGeometryChanges, allow)
            point.edit_mode = allow

    def extend_from_points(self, points: [QtCore.QPointF]):
        for point in points:
            self.add_point(point)

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

