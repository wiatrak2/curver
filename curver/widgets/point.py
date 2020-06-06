from copy import deepcopy

from PyQt5 import QtWidgets, QtGui, QtCore

from curver.widgets import Item


class Point(QtWidgets.QGraphicsEllipseItem, Item):
    SIZE = 4

    def __init__(
        self,
        point: QtCore.QPointF,
        pen: QtGui.QPen = None,
        brush: QtGui.QBrush = None,
        *args,
        **kwargs,
    ):
        self.point = point
        x, y = point.x(), point.y()
        size_offset = self.SIZE / 2
        super().__init__(
            x - size_offset, y - size_offset, self.SIZE, self.SIZE, *args, **kwargs
        )

        self.edit_mode = False

        self.pen = pen
        self.brush = brush
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
        return new_point

    def _setup_appearance(self):
        if self.pen is None:
            self.pen = QtGui.QPen(QtCore.Qt.red)
            self.pen.setWidth(3)
        if self.brush is None:
            self.brush = QtGui.QBrush(QtCore.Qt.black)
        self.setPen(self.pen)
        self.setBrush(self.brush)

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
