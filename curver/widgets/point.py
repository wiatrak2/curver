from PyQt5 import QtWidgets, QtGui, QtCore

from widgets.segment import Segment

class Point(QtWidgets.QGraphicsEllipseItem):
    SIZE = 4
    def __init__(self, point: QtCore.QPointF, *args, **kwargs):
        self.point = point
        x, y = point.x(), point.y()
        size_offset = self.SIZE / 2
        super().__init__(x - size_offset, y - size_offset, self.SIZE, self.SIZE, *args, **kwargs)

        self.associated_segments: [Segment] = []
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

    def __str__(self) -> str:
        return f"Point({self.x},{self.y})"

    def _setup_appearance(self):
        point_pen = QtGui.QPen(QtCore.Qt.red)
        point_pen.setWidth(3)
        point_brush = QtGui.QBrush(QtCore.Qt.black)
        self.setPen(point_pen)
        self.setBrush(point_brush)

    def add_segment(self, segment):
        self.associated_segments.append(segment)

    def change_position(self, vec: QtCore.QPointF):
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
            for segment in self.associated_segments:
                segment.notify_point_change(new_pos, new_pos)
            self.point = new_pos.point
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        return super().mouseReleaseEvent(event)
