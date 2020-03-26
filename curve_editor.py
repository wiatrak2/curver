from enum import Enum
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from ui.main_ui import Ui_MainWindow
from curve_edit_list import CurveEditWindow
from curves import Curve, Polyline
from widgets.scene import CurverGraphicsScene

class CurveEditor(QtWidgets.QMainWindow):
    class _Modes(Enum):
        NONE = 0
        ADD = 1
        EDIT = 2
        DELETE = 3
    modes = _Modes

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._setup_editor_ui()

        self.curves = {}
        self.edited_curve = None

        self.mode = self.modes.NONE

        self.edit_curves_list = CurveEditWindow(self)

    @property
    def plane(self) -> CurverGraphicsScene:
        return self.ui.plane.scene()

    # Setup methods

    def _setup_editor_ui(self):
        self.ui.addPointBox.setHidden(True)
        canvas = self._create_canvas()
        self.ui.plane.setScene(canvas)
        self.ui.plane.scale(1, -1)
        self._connect_actions()

    def _create_canvas(self) -> QtWidgets.QGraphicsScene:
        scene = CurverGraphicsScene(parent=self)
        scene.setSceneRect(-25, -25, 500, 500)
        scene.setBackgroundBrush(QtCore.Qt.white)
        scene.addLine(0,-1000,0,1000)
        scene.addLine(-1000,0,1000,0)
        return scene

    def _connect_actions(self):
        self.ui.addCurveButton.clicked.connect(self.add_curve_button_action)
        self.ui.addPointButton.clicked.connect(self.add_point_button_action)
        self.ui.undoAddPointButton.clicked.connect(self.undo_add_point_button_action)
        self.ui.cancelAddCurveButton.clicked.connect(self.cancel_add_curve_button_action)
        self.ui.saveCurveButton.clicked.connect(self.save_curve_button_action)
        self.ui.editCurveButton.clicked.connect(self.edit_curve_button_action)

    # Button actions

    def add_curve_button_action(self):
        self.ui.addPointBox.setHidden(False)
        curve_type = self.ui.setCurveType.currentText()
        curve_id = f"{curve_type}_{len(self.curves)+1}"  # TODO: unique names, even after removing curve
        self.ui.curveName.setText(curve_id)
        self.edited_curve = Polyline(curve_id)
        self.mode = self.modes.ADD
        self.plane.notify_click = True

    def add_point_scene_click_action(self, point: QtCore.QPointF):
        scene = self.plane
        self.edited_curve.add_point(point, scene)

    def add_point_button_action(self):
        x, y = float(self.ui.xPos.text()), float(self.ui.yPos.text())
        scene = self.plane
        point = QtCore.QPointF(x, y)
        self.edited_curve.add_point(point, scene)

    def undo_add_point_button_action(self):
        if len(self.edited_curve.points):
            scene = self.plane
            self.edited_curve.remove_point(self.edited_curve.points[-1], scene)

    def cancel_add_curve_button_action(self):
        scene = self.plane
        self.edited_curve.delete_curve(scene)
        self.edited_curve = None
        self.ui.addPointBox.setHidden(True)
        self.mode = self.modes.NONE
        self.plane.notify_click = False

    def save_curve_button_action(self):
        curve_id = self.ui.curveName.text()
        if curve_id in self.curves:
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setText("Curve with given name already exists")
            msg_box.exec_()
            return
        self.edited_curve.set_name(curve_id)
        self.curves[curve_id] = self.edited_curve
        self.edited_curve = None
        self.ui.addPointBox.setHidden(True)
        self.mode = self.modes.NONE
        self.plane.notify_click = False

    def edit_curve_button_action(self):
        self.edit_curves_list.show(self.curves)

    def manage_curve_edit(self, curve_id: str, allow=True):
        curve = self.curves[curve_id]
        curve.manage_edit(allow=allow)

    def delete_curve(self, curve_id: str):
        curve = self.curves.pop(curve_id)
        curve.delete_curve(self.plane)

    def notify_scene_click(self, point: QtCore.QPointF):
        if self.mode == self.modes.NONE:
            return
        if self.mode == self.modes.ADD:
            return self.add_point_scene_click_action(point)
