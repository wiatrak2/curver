from copy import deepcopy

from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import widgets
from curver.curves import Curve
import numpy as np

class Polyline(Curve):
    type = "Polyline"
    def __init__(self, curve_name: str):
        super().__init__(curve_name)

    def set_mode(self, mode):
        self.mode = mode

    def set_state(self, other):
        self.delete_curve()
        points = [p.point for p in other.points]
        self.extend_from_points(points)
        self.curve_name = other.curve_name

    def add_point(self, point: QtCore.QPointF):
        new_point = widgets.point.Point(point)
        if len(self.points):
            last_point = self.points[-1]
            new_segment = widgets.line.Line(last_point, new_point)
            last_point.add_segment(new_segment)
            new_point.add_segment(new_segment)
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

    def rotate_curve(self, angle: float, curve_positions: [widgets.point.Point]):
        angle = (2 * np.pi) * angle
        point_rotate_about = self.points[0]  # TODO: allow rotation over other point
        for (point, position) in zip(self.points, curve_positions):
            point_relative_pos = position - point_rotate_about
            new_x = round(point_relative_pos.x * np.cos(angle) - point_relative_pos.y * np.sin(angle), 2)
            new_y = round(point_relative_pos.x * np.sin(angle) + point_relative_pos.y * np.cos(angle), 2)
            point.set_scene_pos(QtCore.QPointF(new_x, new_y) + point_rotate_about.point)

    def scale_curve(self, scale_factor: float, curve_positions: [widgets.point.Point], *args, **kwargs):
         for i, (point, position) in enumerate(zip(self.points[1:], curve_positions[1:])):
            pos_vec_to_prev = position - curve_positions[i]
            scaled_vec = pos_vec_to_prev * scale_factor
            new_pos = self.points[i] + scaled_vec
            point.set_scene_pos(new_pos.point)

    def delete_curve(self):
        while len(self.points):
            point = self.points.pop()
        while len(self.segments):
            segment = self.segments.pop()

    def display(self, scene: QtWidgets.QGraphicsScene):
        for item in self.points + self.segments:
            scene.addItem(item)