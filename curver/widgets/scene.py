from PyQt5 import QtWidgets

class CurverGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notify_click = False
        self.notify_position = False

    def mouseMoveEvent(self, event):
        if self.notify_position:
            self.parent().notify_scene_pos(event.scenePos())
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.notify_click:
            self.parent().notify_scene_click(event.scenePos())
        return super().mousePressEvent(event)
