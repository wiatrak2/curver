from enum import Enum
from dataclasses import dataclass

from PyQt5 import QtWidgets

from curver.curves import Curve


class ControllerModes(Enum):
    NONE = 0
    ADD = 1
    EDIT = 2


@dataclass
class CurveFunctionality:
    weighted: bool = False
    degree_modifier: bool = False
    smooth_join: bool = False

    @classmethod
    def get_functionalities(cls, curve: Curve):
        return CurveFunctionality(
            weighted=curve.weighted,
            degree_modifier=curve.type == "Bezier",
            smooth_join=curve.type == "Bezier",
        )


def set_widget_geometry(
    child: QtWidgets.QWidget, parent: QtWidgets.QWidget, mode="left"
):
    c_w, c_h = child.width(), child.height()
    p_w, p_h = parent.width(), parent.height()
    p_x, p_y = parent.geometry().x(), parent.geometry().y()
    if mode == "left":
        offset = (p_h - c_h) / 2
        child.setGeometry(p_x - c_w, p_y + offset, c_w, c_h)
    elif mode == "right":
        offset = (p_h - c_h) / 2
        child.setGeometry(p_x + p_w, p_y + offset, c_w, c_h)
    elif mode == "top":
        offset = (p_w - c_w) / 2
        child.setGeometry(p_x + offset, p_y + c_h, c_w, c_h)
    elif mode == "bottom":
        offset = (p_w - c_w) / 2
        child.setGeometry(p_x + offset, p_y - c_h, c_w, c_h)
    else:
        child.setGeometry(p_x, p_y, c_w, c_h)
