from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import widgets, utils

class Curve:
    modes = utils.CurveModes
    type = "Curve"
    def __init__(self, curve_name: str):
        self.curve_name = curve_name

        self.mode = self.modes.NONE

        self.points: [QtCore.QPointF] = []

    @property
    def id(self) -> str:
        return self.curve_name

    def set_mode(self, mode):
        raise NotImplementedError

    def set_state(self, other):
        raise NotImplementedError

    def add_point(self, point: QtCore.QPointF):
        raise NotImplementedError

    def delete_point(self, point: QtCore.QPointF):
        raise NotImplementedError

    def rotate_curve(self, angle: float, *args, **kwargs):
        raise NotImplementedError

    def scale_curve(self, scale_factor: float, *args, **kwargs):
        raise NotImplementedError

    def delete_curve(self):
        raise NotImplementedError

    def get_items(self) -> [QtWidgets.QGraphicsItem]:
        raise NotImplementedError
