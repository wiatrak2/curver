import json
import logging
from enum import Enum

import daiquiri
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import curves, widgets, utils
from curver.ui.main_ui import Ui_MainWindow
from curver.curve_edit_list import CurvesListWindow
from curver.curve_edit_window import CurveEditWindow

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)

class CurveEditor(QtWidgets.QMainWindow):
    class _Modes(Enum):
        NONE = 0
        ADD = 1
        EDIT = 2
    modes = _Modes

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._setup_editor_ui()

        self.curves = {}
        self.edited_curve = None

        self.mode = self.modes.NONE

        self.edit_curves_list = CurvesListWindow(self)
        self.edit_curve_window = None

    @property
    def plane(self) -> widgets.scene.CurverGraphicsScene:
        return self.ui.plane.scene()

    # Setup methods

    def _setup_editor_ui(self):
        self.ui.addPointBox.setHidden(True)
        canvas = self._create_canvas()
        self.ui.plane.setScene(canvas)
        self.ui.plane.scale(1, -1)
        self.ui.plane.setMouseTracking(True)
        self._connect_actions()


    def _create_canvas(self) -> QtWidgets.QGraphicsScene:
        scene = widgets.scene.CurverGraphicsScene(parent=self)
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
        self.ui.actionImportCurve.triggered.connect(self.import_curve_action)

    def _set_mode(self, mode):
        self.mode = mode
        if self.mode == self.modes.NONE:
            self.plane.notify_click = False
            self.plane.notify_position = False
        elif self.mode == self.modes.ADD or self.mode == self.modes.EDIT:
            self.plane.notify_click = True
            self.plane.notify_position = True

    # Button actions

    def add_curve_button_action(self):
        self.ui.addPointBox.setHidden(False)
        curve_type = self.ui.setCurveType.currentText()
        curve_id = f"{curve_type}_{len(self.curves)+1}"  # TODO: unique names, even after removing curve
        self.ui.curveName.setText(curve_id)
        self.edited_curve = curves.Polyline(curve_id, self.plane)  # TODO: allow other curves
        self._set_mode(self.modes.ADD)

    def add_point_button_action(self):
        x, y = float(self.ui.xPos.text()), float(self.ui.yPos.text())
        point = QtCore.QPointF(x, y)
        self.edited_curve.add_point(point)

    def undo_add_point_button_action(self):
        if len(self.edited_curve.points):
            self.edited_curve.delete_point(self.edited_curve.points[-1])

    def cancel_add_curve_button_action(self):
        self.edited_curve.delete_curve()
        self.edited_curve = None
        self.ui.addPointBox.setHidden(True)
        self._set_mode(self.modes.NONE)

    def save_curve_button_action(self):
        curve_name = self.ui.curveName.text()
        if curve_name in self.curves:
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setText("Curve with given name already exists")
            msg_box.exec_()
            return

        self.edited_curve.curve_name = curve_name
        self.curves[curve_name] = self.edited_curve
        self.edited_curve = None

        self.ui.addPointBox.setHidden(True)
        self._set_mode(self.modes.NONE)

    def edit_curve_button_action(self):
        utils.set_widget_geometry(self.edit_curves_list, self, mode="left")
        self.edit_curves_list.show(self.curves)

    def import_curve_action(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Import curve", filter="*.json")
        self._import_curve(filename[0])

    def _import_curve(self, filename):
        logger.info(f"Importing curve from {filename}.")
        try:
            with open(filename, "r") as f:
                curve_info = json.load(f)
        except:
            logger.warning(f"Could not load curve from {filename}.")
            return
        curve_cls = curves.types[curve_info.get("type", curves.Curve)]
        curve_name = curve_info.get("curve_name", "")
        curve_points = [QtCore.QPointF(x, y) for (x, y) in curve_info.get("points", [])]
        curve = curve_cls(curve_name, self.plane)
        curve.extend_from_points(curve_points)
        self.curves[curve_name] = curve
        logger.info(f"Curve {curve_name} of type {curve.type} with {len(curve_points)} points defined successfully imported.")
        self._set_mode(self.modes.NONE)

    def manage_curve_edit(self, curve_id: str, allow=True):
        self._set_mode(self.modes.EDIT)

        self.edited_curve = self.curves.pop(curve_id)
        self.edited_curve.manage_edit(allow=allow)
        self.edit_curve_window = CurveEditWindow(self.edited_curve, parent=self)
        utils.set_widget_geometry(self.edit_curve_window, self, mode="left")

        self.edit_curve_window.show()
        self.edit_curves_list.close()

    def finish_curve_edit(self):
        self.curves[self.edited_curve.curve_name] = self.edited_curve
        self._set_mode(self.modes.NONE)
        self.edited_curve.manage_edit(allow=False)
        self.edited_curve = None

    def delete_curve(self, curve_id: str):
        curve = self.curves.pop(curve_id)
        curve.delete_curve()

    # Notifications from scene handling

    def _add_curve_scene_click_action(self, point: QtCore.QPointF):
        self.edited_curve.add_point(point)

    def _add_curve_scene_move_action(self, point: QtCore.QPointF):
        x, y = point.x(), point.y()
        self.ui.xPos.setText(str(int(x)))
        self.ui.yPos.setText(str(int(y)))

    def _edit_curve_scene_move_action(self, point: QtCore.QPointF):
        self.edit_curve_window.notify_scene_pos(point)

    def _edit_curve_scene_click_action(self, point: QtCore.QPointF):
        return self.edit_curve_window.mouse_click_action(point)

    def notify_scene_pos(self, point: QtCore.QPointF):
        if self.mode == self.modes.NONE:
            return
        if self.mode == self.modes.ADD:
            return self._add_curve_scene_move_action(point)
        if self.mode == self.modes.EDIT:
            return self._edit_curve_scene_move_action(point)

    def notify_scene_click(self, point: QtCore.QPointF):
        if self.mode == self.modes.NONE:
            return
        if self.mode == self.modes.ADD:
            return self._add_curve_scene_click_action(point)
        if self.mode == self.modes.EDIT:
            return self._edit_curve_scene_click_action(point)
