import logging
from copy import deepcopy

import daiquiri
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from curver import widgets
from curver.curves import Lagrange

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)


class CubicSpline(Lagrange):
    type = "Cubic Spline"

    def _interpolate(self, n, *args, **kwargs):
        """
        https://stackoverflow.com/a/48085583/12350529
        """
        xs = np.array([p.x() for p in self.points])
        ys = np.array([p.y() for p in self.points])

        t = np.linspace(xs[0], xs[-1], n)

        size = len(xs)

        xdiff = np.diff(xs)
        ydiff = np.diff(ys)

        # allocate buffer matrices
        Li = np.empty(size)
        Li_1 = np.empty(size-1)
        z = np.empty(size)

        # fill diagonals Li and Li-1 and solve [L][y] = [B]
        Li[0] = np.sqrt(2*xdiff[0])
        Li_1[0] = 0.0
        B0 = 0.0 # natural boundary
        z[0] = B0 / Li[0]

        for i in range(1, size-1, 1):
            Li_1[i] = xdiff[i-1] / Li[i-1]
            Li[i] = np.sqrt(2*(xdiff[i-1]+xdiff[i]) - Li_1[i-1] * Li_1[i-1])
            Bi = 6*(ydiff[i]/xdiff[i] - ydiff[i-1]/xdiff[i-1])
            z[i] = (Bi - Li_1[i-1]*z[i-1])/Li[i]

        i = size - 1
        Li_1[i-1] = xdiff[-1] / Li[i-1]
        Li[i] = np.sqrt(2*xdiff[-1] - Li_1[i-1] * Li_1[i-1])
        Bi = 0.0 # natural boundary
        z[i] = (Bi - Li_1[i-1]*z[i-1])/Li[i]

        # solve [L.T][x] = [y]
        i = size-1
        z[i] = z[i] / Li[i]
        for i in range(size-2, -1, -1):
            z[i] = (z[i] - Li_1[i-1]*z[i+1])/Li[i]

        # find index
        index = xs.searchsorted(t)
        np.clip(index, 1, size-1, index)

        xi1, xi0 = xs[index], xs[index-1]
        yi1, yi0 = ys[index], ys[index-1]
        zi1, zi0 = z[index], z[index-1]
        hi1 = xi1 - xi0

        # calculate cubic
        f_t = zi0/(6*hi1)*(xi1-t)**3 + \
            zi1/(6*hi1)*(t-xi0)**3 + \
            (yi1/hi1 - zi1*hi1/6)*(t-xi0) + \
            (yi0/hi1 - zi0*hi1/6)*(xi1-t)

        return [widgets.Point(QtCore.QPointF(t[i], f_t[i])) for i in range(len(t))]

    def get_items(
        self,
        n=1000,
        control_points_line=True,
        points_pen: QtGui.QPen = None,
        segments_pen: QtGui.QPen = None,
        control_points_line_pen: QtGui.QPen = None,
        *args,
        **kwargs
    ) -> (
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
        [QtWidgets.QGraphicsItem],
    ):
        control_points = [widgets.Point(p, pen=points_pen) for p in self.points]
        points = self._interpolate(n)
        lines = [
            widgets.Line(points[i], points[i + 1], pen=segments_pen)
            for i in range(len(points) - 1)
        ]

        angle = 360 * self._rotation_angle
        for point in control_points + points:
            point.setTransformOriginPoint(self.points[0])
            point.setRotation(angle)
            point.setScale(self._scale_factor)
        for line in lines:
            line.setTransformOriginPoint(self.points[0])
            line.setRotation(angle)
            line.setScale(self._scale_factor)

        return control_points, lines, []
