from PyQt5 import QtWidgets, QtCore

from curver.widgets.segment import Segment

class GroupSegment(QtWidgets.QGraphicsItemGroup, Segment):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
