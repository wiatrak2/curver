from PyQt5 import QtWidgets, QtCore

from curver.widgets import Item

class Segment(QtWidgets.QGraphicsLineItem, Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def notify_point_change(self, old_point: QtCore.QPointF, new_point: QtCore.QPointF):
        raise NotImplementedError
