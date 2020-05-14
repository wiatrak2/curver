import logging
from copy import deepcopy

import daiquiri
from PyQt5 import QtCore, QtWidgets, QtGui

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

    def get_items(
        self,
        convex_hull=False,
        points_pen: QtGui.QPen = None,
        segments_pen: QtGui.QPen = None,
        convex_hull_pen: QtGui.QPen = None,
        *args,
        **kwargs
    ) -> (
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
    ):
        points = [widgets.point.Point(p, pen=points_pen) for p in self.points]
        lines = [
            widgets.line.Line(points[i], points[i + 1], pen=segments_pen)
            for i in range(len(points) - 1)
        ]

        extra_segments = []
        if convex_hull:
            if convex_hull_pen is None:
                convex_hull_pen = QtGui.QPen(QtGui.QColor(34, 153, 84))
            convex_hull_points = self._get_convex_hull()
            n = len(convex_hull_points)
            extra_segments += [
                widgets.Line(
                    widgets.Point(convex_hull_points[i]),
                    widgets.Point(convex_hull_points[(i+1) % n]),
                    pen=convex_hull_pen
                )
            for i in range(n)]
        return points, lines, extra_segments
