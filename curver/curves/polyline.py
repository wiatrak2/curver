import logging
from copy import deepcopy

import daiquiri
from PyQt5 import QtCore, QtWidgets

from curver import widgets
from curver.curves import BaseCurve

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)

class Polyline(BaseCurve):
    type = "Polyline"
    def __init__(self, curve_id: str):
        super().__init__(curve_id)
        self._edition_relative_position: [QtCore.QPointF] = None

    def set_mode(self, mode):
        self.mode = mode
        if mode == self.modes.ROTATE_CURVE or mode == self.modes.SCALE_CURVE:
            self._edition_relative_position = deepcopy(self.points)

    def get_items(self, *args, **kwargs) -> [QtWidgets.QGraphicsItem]:
        points = [widgets.point.Point(p) for p in self.points]
        lines = [widgets.line.Line(points[i], points[i+1]) for i in range(len(points)-1)]
        return points, lines
