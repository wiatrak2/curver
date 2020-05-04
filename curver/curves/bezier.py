import logging
import scipy.special
from copy import deepcopy

import daiquiri
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from curver import widgets
from curver.curves import BaseCurve

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)


class Bezier(BaseCurve):
    type = "Bezier"

    def __init__(self, curve_id: str):
        super().__init__(curve_id)
        self._edition_relative_position: [QtCore.QPointF] = None

    def set_mode(self, mode):
        if mode == self.modes.ROTATE_CURVE or mode == self.modes.SCALE_CURVE:
            self._edition_relative_position = deepcopy(self.points)
        self.mode = mode

    @staticmethod
    def _bernstein(n, i, t):
        return scipy.special.binom(n, i) * np.power(t, i) * np.power(1 - t, n - i)

    def _interpolate(self, x, *args, **kwargs):
        xs = np.array([p.x() for p in self.points])
        ys = np.array([p.y() for p in self.points])
        bernsteins = np.array(
            [
                self._bernstein(len(self.points) - 1, i, x)
                for i in range(len(self.points))
            ]
        )
        new_x = np.sum(xs * bernsteins)
        new_y = np.sum(ys * bernsteins)
        return QtCore.QPointF(new_x, new_y)

    def get_items(
        self,
        n=1000,
        control_points_line=True,
        points_pen: QtGui.QPen = None,
        segments_pen: QtGui.QPen = None,
        control_points_line_pen: QtGui.QPen = None,
        *args,
        **kwargs
    ) -> (
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
    ):
        control_points = [widgets.Point(p, pen=points_pen) for p in self.points]
        points = [widgets.Point(self.points[0])]
        segments = []

        for t in range(n):
            x = t / (n - 1)
            point = widgets.Point(self._interpolate(x))
            points.append(point)

        lines = [
            widgets.Line(points[i], points[i + 1], pen=segments_pen)
            for i in range(len(points) - 1)
        ]

        control_points_lines = []
        if control_points_line:
            if control_points_line_pen is None:
                control_points_line_pen = QtGui.QPen(QtCore.Qt.gray)
                control_points_line_pen.setDashPattern([5, 5])
            control_points_lines = [
                widgets.Line(
                    control_points[i],
                    control_points[i + 1],
                    pen=control_points_line_pen,
                )
                for i in range(len(control_points) - 1)
            ]

        return control_points, lines, control_points_lines
