import logging
import scipy.special

import daiquiri
import numpy as np
from PyQt5 import QtCore

from curver.curves import Bezier

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)


class RationalBezier(Bezier):
    type = "Rational Bezier"

    weighted = True

    def __init__(self, curve_id: str):
        super().__init__(curve_id)
        self.weights = []

    @property
    def _weights(self) -> [float]:
        return self.weights

    def set_points(self, points: [QtCore.QPointF], weights: [float] = None):
        super().set_points(points)
        if weights is None:
            weights = list(np.ones_like(points))
        self.weights = weights

    def add_point(self, point: QtCore.QPointF, weight: float = 1.0):
        logger.info(f"Point {point} weight: {weight}")
        super().add_point(point)
        self.weights.append(weight)

    def delete_point(self, point: QtCore.QPointF, *args, **kwargs):
        if point in self.points:
            point_idx = self.points.index(point)
            self.points.remove(point)
            self.weights.pop(point_idx)

    def edit_weight(self, point: QtCore.QPointF, weight: float, *args, **kwargs):
        if point in self.points:
            point_idx = self.points.index(point)
            self.weights[point_idx] = weight

    def merge_points(self, points: [QtCore.QPointF], weights: [float] = None):
        super().merge_points(points)
        if weights is None:
            weights = list(np.ones_like(points))
        self.weights += weights

    def permute_points(
        self, point_1: QtCore.QPointF, point_2: QtCore.QPointF, *args, **kwargs
    ):
        if point_1 in self.points and point_2 in self.points:
            p_1_idx, p_2_idx = self.points.index(point_1), self.points.index(point_2)
            self.points[p_1_idx], self.points[p_2_idx] = (
                self.points[p_2_idx],
                self.points[p_1_idx],
            )
            self.weights[p_1_idx], self.weights[p_2_idx] = (
                self.weights[p_2_idx],
                self.weights[p_1_idx],
            )

    def reverse_curve(self, *args, **kwargs):
        super().reverse_curve()
        self.weights = self.weights[::-1]

    def delete_curve(self):
        super().delete_curve()
        self.weights = []

    def serialize_curve(self) -> dict:
        curve_dict = super().serialize_curve()
        curve_dict["weights"] = self.weights
        return curve_dict
