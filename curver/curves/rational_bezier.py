import logging
import scipy.special
from copy import deepcopy

import daiquiri
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from curver import widgets
from curver.curves import Bezier

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)


class RationalBezier(Bezier):
    type = "Rational Bezier"

    weighted = True

    def __init__(self, curve_id: str):
        super().__init__(curve_id)
        self.weights = []

    def set_points(self, points: [QtCore.QPointF], weights: [float] = None):
        super().set_points(points)
        if weights is None:
            weights = np.ones_like(points)
        self.weights = weights

    def add_point(self, point: QtCore.QPointF, weight: float = 1.):
        logger.info(f"Point {point} weight: {weight}")
        super().add_point(point)
        self.weights.append(weight)

    def add_points(self, points: [QtCore.QPointF], weights: [float] = None):
        super().add_points(points)
        if weights is None:
            weights = np.ones_like(points)
        self.weights += weights

    def _interpolate(self, x, *args, **kwargs):
        xs = np.array([p.x() for p in self.points])
        ys = np.array([p.y() for p in self.points])
        bernsteins = np.array(
            [
                self._bernstein(len(self.points) - 1, i, x)
                for i in range(len(self.points))
            ]
        )
        new_x = np.sum(xs * bernsteins * self.weights) / np.sum(bernsteins * self.weights)
        new_y = np.sum(ys * bernsteins * self.weights) / np.sum(bernsteins * self.weights)
        return QtCore.QPointF(new_x, new_y)

    def serialize_curve(self) -> dict:
        curve_dict = super().serialize_curve()
        curve_dict["weights"]: self.weights
        return curve_dict
