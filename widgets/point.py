from PyQt5 import QtWidgets, QtGui

class Point(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit_mode = False
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)

    def mousePressEvent(self, event):
        print("CLICK!")
        self.edit_mode = True
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        print("RELEASE")
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        if self.edit_mode:
            new_pos = event.scenePos()
            new_x, new_y = new_pos.x(), new_pos.y()
            self.x = new_x
            self.y = new_y
        return super().mouseReleaseEvent(event)
