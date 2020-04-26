from copy import deepcopy

from PyQt5 import QtWidgets, QtGui, QtCore

from curver.widgets import Item

class Point(QtWidgets.QGraphicsEllipseItem, Item):
    SIZE = 4
    def __init__(self, point: QtCore.QPointF, *args, **kwargs):
        self.point = point
        x, y = point.x(), point.y()
        size_offset = self.SIZE / 2
        super().__init__(x - size_offset, y - size_offset, self.SIZE, self.SIZE, *args, **kwargs)

        self.edit_mode = False

        self._setup_appearance()

    @property
    def x(self):
        return self.point.x()

    @property
    def y(self):
        return self.point.y()

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.point == other.point
        if isinstance(other, QtCore.QPointF):
            return self.point == other
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"Point({self.x},{self.y})"

    def __repr__(self) -> str:
        return str(self)

    def __sub__(self, other):
        return Point(self.point - other.point)

    def __add__(self, other):
        return Point(self.point + other.point)

    def __mul__(self, scalar: float):
        return Point(self.point * scalar)

    def __deepcopy__(self, memo):
        new_point = Point(self.point)
        new_point.edit_mode = self.edit_mode
        new_point.associated_segments = self.associated_segments
        return new_point

    def _setup_appearance(self):
        point_pen = QtGui.QPen(QtCore.Qt.red)
        point_pen.setWidth(3)
        point_brush = QtGui.QBrush(QtCore.Qt.black)
        self.setPen(point_pen)
        self.setBrush(point_brush)

    def set_scene_pos(self, point: QtCore.QPointF):
        pos_change = point - self.point
        return self.move_by_vector(pos_change)

    def move_by_vector(self, vec: QtCore.QPointF):
        new_pos = self.point + vec
        new_point = Point(new_pos)
        for segment in self.associated_segments:
            segment.notify_point_change(self, new_point)
        self.moveBy(vec.x(), vec.y())
        self.point = new_pos

    def mousePressEvent(self, event):
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.edit_mode:
            new_pos = Point(event.scenePos())
            for controller in self.controllers:
                controller.notify_point_change(self, new_pos)
            self.point = new_pos.point
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        return super().mouseReleaseEvent(event)
