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
        self.t = np.array([])
        self.curve_points = []

    def set_mode(self, mode):
        if mode == self.modes.ROTATE_CURVE or mode == self.modes.SCALE_CURVE:
            self._edition_relative_position = deepcopy(self.points)
        self.mode = mode

    def de_casteljau(self, t):
        n = len(self.points)
        W_k_i = np.empty((n, n), dtype=QtCore.QPointF)
        W_k_i[0, :] = self.points
        for k in range(1, n):
            for i in range(n - k):
                W_k_i[k][i] = (1 - t) * W_k_i[k - 1][i] + t * W_k_i[k - 1][i + 1]
        return W_k_i[n - 1][0], W_k_i

    def split_curve(self, point: QtCore.QPointF, *args, **kwargs):
        nearest_point = None
        nearest_dist = 1e100
        for p in self.curve_points:
            dist_square = np.power(p.x - point.x(), 2) + np.power(p.y - point.y(), 2)
            if dist_square < nearest_dist:
                nearest_point = p
                nearest_dist = dist_square
        point_idx = self.curve_points.index(nearest_point)
        t = self.t[point_idx]
        _, W_k_i = self.de_casteljau(t)
        curve_L_points = list(W_k_i[:, 0])
        curve_R_points = [
            W_k_i[len(self.points) - 1 - i][i] for i in range(len(self.points))
        ]
        curve_L = self.construct_from_points(f"{self.curve_id}_L", curve_L_points)
        curve_R = self.construct_from_points(f"{self.curve_id}_R", curve_R_points)
        return curve_L, curve_R

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
        convex_hull=False,
        points_pen: QtGui.QPen = None,
        segments_pen: QtGui.QPen = None,
        control_points_line_pen: QtGui.QPen = None,
        convex_hull_pen: QtGui.QPen = None,
        *args,
        **kwargs,
    ) -> (
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
    ):
        control_points = [widgets.Point(p, pen=points_pen) for p in self.points]
        self.curve_points = [widgets.Point(self.points[0])]

        self.t = np.linspace(0, 1, n)
        self.curve_points = [widgets.Point(self._interpolate(x)) for x in self.t]

        lines = [
            widgets.Line(
                self.curve_points[i], self.curve_points[i + 1], pen=segments_pen
            )
            for i in range(len(self.curve_points) - 1)
        ]

        extra_segments = []
        if control_points_line:
            if control_points_line_pen is None:
                control_points_line_pen = QtGui.QPen(QtCore.Qt.gray)
                control_points_line_pen.setDashPattern([5, 5])
            extra_segments += [
                widgets.Line(
                    control_points[i],
                    control_points[i + 1],
                    pen=control_points_line_pen,
                )
                for i in range(len(control_points) - 1)
            ]
        if convex_hull:
            if convex_hull_pen is None:
                convex_hull_pen = QtGui.QPen(QtGui.QColor(34, 153, 84))
            convex_hull_points = self._get_convex_hull()
            n = len(convex_hull_points)
            extra_segments += [
                widgets.Line(
                    widgets.Point(convex_hull_points[i]),
                    widgets.Point(convex_hull_points[(i + 1) % n]),
                    pen=convex_hull_pen,
                )
                for i in range(n)
            ]

        return control_points, lines, extra_segments
