from PyQt5 import uic, QtWidgets, QtGui, QtCore

class Curve:
    def __init__(self, curve_name):
        self.curve_name = curve_name
        self.points = []

        self.drawn_points = []
        self.drawn_segments = []

    def set_name(self, name: str):
        self.name = name

    def add_point(self, point: QtCore.QPointF, scene: QtWidgets.QGraphicsScene):
        raise NotImplementedError

    def delete_curve(self, scene: QtWidgets.QGraphicsScene):
        raise NotImplementedError

class Polyline(Curve):
    type = "Polyline"
    def __init__(self, curve_name):
        super().__init__(curve_name)

        self.pointPen = QtGui.QPen(QtCore.Qt.red)
        self.pointPen.setWidth(3)

        self.segmentPen = QtGui.QPen(QtCore.Qt.black)

    def add_point(self, point: QtCore.QPointF, scene: QtWidgets.QGraphicsScene):
        x, y = point.x(), point.y()
        self.drawn_points.append(scene.addEllipse(x, y, 2, 2, pen=self.pointPen))
        if len(self.points):
            last_point = self.points[-1]
            last_x, last_y = last_point.x(), last_point.y()
            self.drawn_segments.append(scene.addLine(last_x, last_y, x, y, pen=self.segmentPen))
        self.points.append(point)

    def delete_curve(self, scene: QtWidgets.QGraphicsScene):
        while len(self.drawn_points):
            point = self.drawn_points.pop()
            scene.removeItem(point)
        while len(self.drawn_segments):
            segment = self.drawn_segments.pop()
            scene.removeItem(segment)

