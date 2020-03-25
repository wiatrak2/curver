from PyQt5 import QtWidgets

class CurverGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notify_click = False

    def mousePressEvent(self, event):
        if self.notify_click:
            self.parent().add_point_scene_click_action(event.scenePos())
        return super().mousePressEvent(event)
