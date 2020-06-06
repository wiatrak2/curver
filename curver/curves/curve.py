from PyQt5 import QtWidgets, QtCore

from curver import widgets
from curver.curves import utils


class Curve:
    type = "Curve"

    modes = utils.CurveModes
    weighted = False

    def __init__(self, curve_id: str):
        self.curve_id = curve_id

        self.mode = self.modes.NONE

        self.points: [QtCore.QPointF] = []

    @property
    def is_movable(self) -> bool:
        return True

    @property
    def id(self) -> str:
        return self.curve_id

    def __str__(self) -> str:
        return f"[{self.type}] {self.id}"

    @classmethod
    def construct_from_points(cls, curve_id: str, points: [QtCore.QPointF]):
        raise NotImplementedError

    def set_mode(self, mode, *args, **kwargs):
        raise NotImplementedError

    def set_state(self, other, *args, **kwargs):
        raise NotImplementedError

    def set_points(self, points: [QtCore.QPointF], *args, **kwargs):
        raise NotImplementedError

    def add_point(self, point: QtCore.QPointF, *args, **kwargs):
        raise NotImplementedError

    def delete_point(self, point: QtCore.QPointF, *args, **kwargs):
        raise NotImplementedError

    def edit_weight(self, point: QtCore.QPointF, weight: float, *args, **kwargs):
        raise NotImplementedError

    def move_point(
        self, point: QtCore.QPointF, vector: QtCore.QPointF, *args, **kwargs
    ):
        raise NotImplementedError

    def merge_points(self, points: [QtCore.QPointF], *args, **kwargs):
        raise NotImplementedError

    def permute_points(
        self, point_1: QtCore.QPointF, point_2: QtCore.QPointF, *args, **kwargs
    ):
        raise NotImplementedError

    def move_curve(self, vector: QtCore.QPointF, *args, **kwargs):
        raise NotImplementedError

    def reverse_curve(self, *args, **kwargs):
        raise NotImplementedError

    def rotate_curve(self, angle_factor: float, *args, **kwargs):
        raise NotImplementedError

    def scale_curve(self, scale_factor: float, *args, **kwargs):
        raise NotImplementedError

    def delete_curve(self):
        raise NotImplementedError

    def split_curve(self, point: QtCore.QPointF, *args, **kwargs):
        raise NotImplementedError

    def get_nearest_point(self, point: widgets.Point) -> QtCore.QPointF:
        raise NotImplementedError

    def _get_convex_hull(self) -> [QtCore.QPointF]:
        raise NotImplementedError

    def get_items(
        self, *args, **kwargs
    ) -> (
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
    ):
        raise NotImplementedError

    def serialize_curve(self) -> dict:
        return {
            "type": self.type,
            "id": self.curve_id,
            "points": [[p.x(), p.y()] for p in self.points],
        }
