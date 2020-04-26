from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import widgets, utils

class Curve:
    modes = utils.CurveModes
    type = "Curve"
    def __init__(self, curve_id: str):
        self.curve_id = curve_id

        self.mode = self.modes.NONE

        self.points: [QtCore.QPointF] = []

    @property
    def id(self) -> str:
        return self.curve_id

    def set_mode(self, mode):
        raise NotImplementedError

    def set_state(self, other):
        raise NotImplementedError

    def set_points(self, points: [QtCore.QPointF]):
        raise NotImplementedError

    def add_point(self, point: QtCore.QPointF):
        raise NotImplementedError

    def delete_point(self, point: QtCore.QPointF):
        raise NotImplementedError

    def move_point(self, point: QtCore.QPointF, vector: QtCore.QPointF):
        raise NotImplementedError

    def permute_points(self, point_1: QtCore.QPointF, point_2: QtCore.QPointF):
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

    def get_nearest_point(self, point: widgets.point.Point) -> QtCore.QPointF:
        raise NotImplementedError

    def get_items(self) -> [QtWidgets.QGraphicsItem]:
        raise NotImplementedError

    def serialize_curve(self) -> dict:
        return {
            "type": self.type,
            "_id": self.curve_id,
            "points": [[p.x(), p.y()] for p in self.points],
        }
