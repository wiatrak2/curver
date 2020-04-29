import numpy as np
from copy import deepcopy

from PyQt5 import QtWidgets, QtGui, QtCore

from curver import widgets

class Line(widgets.Segment):
    def __init__(self, point_1: widgets.Point, point_2: widgets.Point, pen: QtGui.QPen = None, *args, **kwargs):
        self.point_1 = point_1
        self.point_2 = point_2
        self.segment = QtCore.QLineF(self.point_1.point, self.point_2.point)
        super().__init__(self.segment, *args, **kwargs)

        self.pen = self._setup_appearance(pen)


    def __hash__(self):
        return hash((self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y))

    def __str__(self) -> str:
        return f"Line({self.point_1}, {self.point_2})"

    def __repr__(self) -> str:
        return str(self)

    def __deepcopy__(self, memo):
        new_line = Line(self.point_1, self.point_2)
        return new_line

    def _setup_appearance(self, pen: QtGui.QPen):
        if pen is None:
            pen = QtGui.QPen(QtCore.Qt.black)
            pen.setWidth(1)
        self.setPen(pen)
        return pen
