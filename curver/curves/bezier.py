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
        self.t_values = np.array([])
        self.curve_points = []

    @property
    def n(self):
        return len(self.points)

    @property
    def _weights(self) -> np.ndarray:
        return np.ones(self.n)

    def set_mode(self, mode):
        if mode == self.modes.ROTATE_CURVE or mode == self.modes.SCALE_CURVE:
            self._edition_relative_position = deepcopy(self.points)
        self.mode = mode

    def smooth_join_curve(self, other):
        move_vec = self.points[-1] - other.points[0]
        other.move_curve(move_vec)
        if len(self.points) >= 2 and len(other.points) >= 2:
            smooth_join_vector = self.points[-1] - self.points[-2]
            other.points[1] = other.points[0] + smooth_join_vector

    def raise_degree(self):
        new_points = [
            i / self.n * self.points[i - 1]
            + (self.n - i) / self.n * self.points[i % self.n]
            for i in range(self.n + 1)
        ]
        self.set_points(new_points)

    def reduce_degree(self):
        new_points_L = [self.points[0]]
        for i in range(1, self.n // 2):
            new_points_L.append(
                (1 + i / (self.n - i)) * self.points[i]
                - i / (self.n - i) * new_points_L[i - 1]
            )
        new_points_R = [self.points[-1]]
        for i in range(self.n - 1, self.n // 2, -1):
            new_points_R.append(
                self.n / i * self.points[i - 1]
                + (1 - self.n / i) * new_points_R[self.n - i - 1]
            )
        middle_point = 0.5 * new_points_L[-1] + 0.5 * new_points_R[-1]
        new_points = new_points_L[:-1] + [middle_point] + new_points_R[:-1][::-1]
        self.set_points(new_points)

    def de_casteljau(self, t):
        W_k_i = np.empty((self.n, self.n), dtype=QtCore.QPointF)
        W_k_i[0, :] = self.points
        for k in range(1, self.n):
            for i in range(self.n - k):
                W_k_i[k][i] = (1 - t) * W_k_i[k - 1][i] + t * W_k_i[k - 1][i + 1]
        return W_k_i[self.n - 1][0], W_k_i

    def split_curve(self, point: QtCore.QPointF, *args, **kwargs):
        nearest_point = None
        nearest_dist = 1e100
        for p in self.curve_points:
            dist_square = np.power(p.x - point.x(), 2) + np.power(p.y - point.y(), 2)
            if dist_square < nearest_dist:
                nearest_point = p
                nearest_dist = dist_square
        point_idx = self.curve_points.index(nearest_point)
        t = self.t_values[point_idx]
        _, W_k_i = self.de_casteljau(t)
        curve_L_points = list(W_k_i[:, 0])
        curve_R_points = [
            W_k_i[len(self.points) - 1 - i][i] for i in range(len(self.points))
        ]
        curve_L = self.construct_from_points(f"{self.curve_id}_L", curve_L_points)
        curve_R = self.construct_from_points(f"{self.curve_id}_R", curve_R_points)
        return curve_L, curve_R

    def _interpolate(self, t: float, *args, **kwargs) -> QtCore.QPointF:
        """
        Computing a point's value on the Bezier curve.
        Method invented by P. Wozny and F. Chudy in "Linear-time geometric algorithm for evaluating Bézier curves" paper.
        """
        h = 1.0
        Q = self.points[0]
        for k in range(1, self.n):
            h = (self._weights[k] * h * t * (self.n - k)) / (
                self._weights[k - 1] * k * (1 - t)
                + self._weights[k] * h * t * (self.n - k)
            )
            Q = (1 - h) * Q + h * self.points[k]
        return Q

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

        self.t_values = np.linspace(0, 1, n)
        self.curve_points = [widgets.Point(self._interpolate(x)) for x in self.t_values]

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
