from enum import Enum


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
