from PyQt5 import QtWidgets, QtCore

class GroupSegment(QtWidgets.QGraphicsItemGroup):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def notify_point_change(self, old_point: QtCore.QPointF, new_point: QtCore.QPointF):
        raise NotImplementedError
