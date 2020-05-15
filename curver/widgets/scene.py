from PyQt5 import QtWidgets, QtCore, QtGui


class CurverGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, width=700, height=500, line_len=1000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notify_click = False
        self.notify_position = False
        self._setup(width, height, line_len)

    def _setup(self, width, height, line_len):
        self.setSceneRect(-10, -10, width, height)
        self.setBackgroundBrush(QtCore.Qt.white)
        for x in range(-line_len, line_len, 10):
            self.addLine(x, -line_len, x, line_len, pen=QtGui.QPen(QtGui.QColor(234, 237, 237)))
            self.addLine(-line_len, x, line_len, x, pen=QtGui.QPen(QtGui.QColor(234, 237, 237)))
        self.addLine(0, -line_len, 0, line_len)
        self.addLine(-line_len, 0, line_len, 0)

    def __deepcopy__(self, memo):
        new_scene = CurverGraphicsScene()
        new_scene.notify_click = self.notify_click
        new_scene.notify_position = self.notify_position
        return new_scene

    def mouseMoveEvent(self, event):
        if self.notify_position:
            self.parent().notify_scene_pos(event.scenePos())
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.notify_click:
            self.parent().mouse_click_action(event.scenePos())
        return super().mousePressEvent(event)
