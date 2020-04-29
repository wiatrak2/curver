import json
import logging
from enum import Enum

import daiquiri
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import curves, widgets, utils, curve_controller
from curver.ui.main_ui import Ui_MainWindow
from curver.curve_edit_list import CurvesListWindow
from curver.curve_edit_window import CurveEditWindow
from copy import deepcopy

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)


class CurveEditor(QtWidgets.QMainWindow):
    modes = utils.ControllerModes

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._setup_editor_ui()

        self.controller = curve_controller.CurveController(self.scene)

        self.mode = self.modes.NONE
        self._update_ui()

        self.edit_curves_list = None
        self.edit_curve_window = None

    @property
    def scene(self) -> widgets.CurverGraphicsScene:
        return self.ui.plane.scene()

    # Setup methods

    def set_mode(self, new_mode):
        self.mode = new_mode
        self._update_ui()

    def _setup_editor_ui(self):
        self.ui.setCurveType.addItems(curves.types.keys())
        canvas = self._create_canvas()
        self.ui.plane.setScene(canvas)
        self.ui.plane.scale(1, -1)
        self.ui.plane.setMouseTracking(True)
        self._connect_actions()

    def _create_canvas(self) -> QtWidgets.QGraphicsScene:
        scene = widgets.CurverGraphicsScene(parent=self)
        scene.setSceneRect(-25, -25, 500, 500)
        scene.setBackgroundBrush(QtCore.Qt.white)
        scene.addLine(0, -1000, 0, 1000)
        scene.addLine(-1000, 0, 1000, 0)
        return scene

    def _connect_actions(self):
        self.ui.addCurveButton.clicked.connect(self.add_curve_button_action)
        self.ui.addPointButton.clicked.connect(self.add_point_button_action)
        self.ui.undoAddPointButton.clicked.connect(self.undo_add_point_button_action)
        self.ui.cancelAddCurveButton.clicked.connect(
            self.cancel_add_curve_button_action
        )
        self.ui.saveCurveButton.clicked.connect(self.save_curve_button_action)
        self.ui.editCurveButton.clicked.connect(self.edit_curve_button_action)
        self.ui.actionImportCurve.triggered.connect(self.import_curve_action)

    def _update_ui(self):
        self.ui.addPointBox.setVisible(self.mode == self.modes.ADD)

    # Button actions

    def add_curve_button_action(self):
        if self.mode == self.modes.NONE:
            self.set_mode(self.modes.ADD)
            curve_type = self.ui.setCurveType.currentText()
            curve_cls = curves.types[curve_type]
            curve_id = f"{curve_type}_{len(self.controller.curves)+1}"  # TODO: unique names, even after removing curve
            self.ui.curveName.setText(curve_id)
            self.controller.create_curve_start(curve_id, curve_cls)

    def add_point_button_action(self):
        x, y = float(self.ui.xPos.text()), float(self.ui.yPos.text())
        point = QtCore.QPointF(x, y)
        self.controller.add_point(point)

    def undo_add_point_button_action(self):
        self.controller.delete_point_idx(-1)

    def cancel_add_curve_button_action(self):
        self.controller.delete_curve()
        self.ui.addPointBox.setHidden(True)

    def save_curve_button_action(self):
        curve_id = self.ui.curveName.text()
        curve_id_success = self.controller.rename_curve(curve_id)
        if not curve_id_success:
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setText("Curve with given name already exists")
            msg_box.exec_()
            return

        self.controller.create_curve_finish()
        self.set_mode(self.modes.NONE)

    def edit_curve_button_action(self):
        if self.mode == self.modes.NONE:
            self.set_mode(self.modes.EDIT)
            self.edit_curves_list = CurvesListWindow(self)
            utils.set_widget_geometry(self.edit_curves_list, self, mode="left")
            self.edit_curves_list.show(self.controller.curves)

    def import_curve_action(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, "Import curve", filter="*.json"
        )
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
        curve_id = curve_info.get("curve_id", "")
        curve_points = [QtCore.QPointF(x, y) for (x, y) in curve_info.get("points", [])]
        self.controller.add_curve(curve_id, curve_cls, curve_points)
        logger.info(
            f"Curve {curve_id} of type {curve_cls.type} with {len(curve_points)} points defined successfully imported."
        )

    def edit_curve_start(self, curve_id: str):
        self.controller.edit_curve_start(curve_id)
        self.edit_curve_window = CurveEditWindow(curve_id, parent=self)
        utils.set_widget_geometry(self.edit_curve_window, self, mode="left")
        self.edit_curve_window.show()

    def edit_curve_finish(self):
        self.controller.edit_curve_finish()
        self.set_mode(self.modes.NONE)

    def edit_curve_list_close(self):
        self.set_mode(self.modes.NONE)

    def delete_curve(self, curve_id: str):
        self.controller.delete_curve(curve_id)

    # Notifications from scene handling

    def _add_curve_scene_click_action(self, point: QtCore.QPointF):
        self.controller.add_point(point)

    def _add_curve_scene_move_action(self, point: QtCore.QPointF):
        x, y = point.x(), point.y()
        self.ui.xPos.setText(str(int(x)))
        self.ui.yPos.setText(str(int(y)))

    def _edit_curve_scene_move_action(self, point: QtCore.QPointF):
        self.edit_curve_window.notify_scene_pos(point)

    def _edit_curve_scene_click_action(self, point: QtCore.QPointF):
        return self.edit_curve_window.mouse_click_action(point)

    def notify_scene_pos(self, point: QtCore.QPointF):
        if self.controller.mode == self.controller.modes.NONE:
            return
        if self.controller.mode == self.controller.modes.ADD:
            return self._add_curve_scene_move_action(point)
        if self.controller.mode == self.controller.modes.EDIT:
            return self._edit_curve_scene_move_action(point)

    def notify_scene_click(self, point: QtCore.QPointF):
        if self.controller.mode == self.controller.modes.NONE:
            return
        if self.controller.mode == self.controller.modes.ADD:
            return self._add_curve_scene_click_action(point)
        if self.controller.mode == self.controller.modes.EDIT:
            return self._edit_curve_scene_click_action(point)
