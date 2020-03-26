from PyQt5 import QtWidgets, QtGui, QtCore

from widgets.segment import Segment

class Line(Segment):
    def __init__(self, point_1: QtCore.QPointF, point_2: QtCore.QPointF, *args, **kwargs):
        self.point_1 = point_1
        self.point_2 = point_2
        self.segment = QtCore.QLineF(self.point_1, self.point_2)
        super().__init__(self.segment, *args, **kwargs)

    def notify_point_change(self, old_point: QtCore.QPointF, new_point: QtCore.QPointF):
        if old_point == self.point_1:
            self.point_1 = new_point
            self.segment.setP1(self.point_1)
        else:
            self.point_2 = new_point
            self.segment.setP2(self.point_2)
        self.setLine(self.segment)


