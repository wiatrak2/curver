from PyQt5 import QtWidgets


class CurverGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notify_click = False
        self.notify_position = False

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
