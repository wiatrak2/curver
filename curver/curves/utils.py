from enum import Enum

import numpy as np
from PyQt5 import QtCore


def dist(point_1: QtCore.QPointF, point_2: QtCore.QPointF) -> float:
    return np.sqrt(
        np.power(point_1.x() - point_2.x(), 2) + np.power(point_1.y() - point_2.y(), 2)
    )


def vector_length(vector: QtCore.QPointF) -> float:
    return np.sqrt(np.power(vector.x(), 2) + np.power(vector.y(), 2))


class CurveModes(Enum):
    NONE = 0
    ADD_POINT = 1
    DELETE_POINT = 2
    MOVE_BY_VECTOR = 3
    PERMUTE_POINTS = 4
    REVERSE_POINTS = 5
    ROTATE_CURVE = 6
    SCALE_CURVE = 7
    EXPORT_CURVE = 8
    JOIN_CURVE = 9
    EDIT_WEIGHT = 10
