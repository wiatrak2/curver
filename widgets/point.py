from PyQt5 import QtWidgets, QtGui, QtCore

from widgets.segment import Segment

class Point(QtWidgets.QGraphicsEllipseItem):
    SIZE = 2
    def __init__(self, point: QtCore.QPointF, *args, **kwargs):
        self.point = point
        x, y = point.x(), point.y()
        super().__init__(x, y, self.SIZE, self.SIZE, *args, **kwargs)

        self.associated_segments: [Segment] = []
        self.edit_mode = False
        self._setup_appearance()

    def _setup_appearance(self):
        point_pen = QtGui.QPen(QtCore.Qt.red)
        point_pen.setWidth(3)
        point_brush = QtGui.QBrush(QtCore.Qt.gray)
        self.setPen(point_pen)
        self.setBrush(point_brush)

    def add_segment(self, segment):
        self.associated_segments.append(segment)

    def mousePressEvent(self, event):
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # TODO: Segments move
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.edit_mode:
            new_pos = event.scenePos()
            for segment in self.associated_segments:
                segment.notify_point_change(self.point, new_pos)
            self.point = new_pos
        return super().mouseReleaseEvent(event)
