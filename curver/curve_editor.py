import json
import logging
from enum import Enum

import daiquiri
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import curves, widgets, utils, curve_controller
from curver.ui.main_ui import Ui_MainWindow
from curver.add_curve_panel import addCurvePanel
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

        self.controller = curve_controller.CurveController(self.scene, main_ui=self)

        self.add_curve_panel = addCurvePanel(self)

        self.mode = self.modes.NONE
        self._update_ui()

        self.current_curve_type = None

        self.edit_curves_list = None
        self.edit_curve_window = None

    @property
    def scene(self) -> widgets.CurverGraphicsScene:
        return self.ui.plane.scene()

    # Setup methods

    def set_mode(self, new_mode):
        self.mode = new_mode
        self._update_ui()

    def set_panel_widget(self, new_widget):
        logger.info(f"Setting panel widget to {new_widget}.")
        current_layout_item = self.ui.panelLayout.itemAt(0)
        if current_layout_item is None:
            self.ui.panelLayout.addWidget(new_widget)
        else:
            current_widget = current_layout_item.widget()
            current_widget.hide()
            self.ui.mainLayout.replaceWidget(current_widget, new_widget)
        new_widget.show()

    def add_to_menu_bar(self, menu):
        return self.ui.menubar.addMenu(menu)

    def _setup_editor_ui(self):
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
        self.ui.actionImportCurve.triggered.connect(self.import_curve_action)

    def _update_ui(self):
        if self.mode == self.modes.NONE:
            self.set_panel_widget(self.add_curve_panel)

    # Button actions

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
        curve_id = curve_info.get("id", "")
        curve_points = [QtCore.QPointF(x, y) for (x, y) in curve_info.get("points", [])]
        curve_weights = None
        if curve_cls.weighted:
            curve_weights = curve_info.get("weights")
        self.controller.create_curve(curve_id, curve_cls, curve_points, weights=curve_weights)
        logger.info(
            f"Curve {curve_id} of type {curve_cls.type} with {len(curve_points)} points successfully imported."
        )

    def edit_curve_start(self, curve_id: str):
        self.set_mode(self.modes.EDIT)
        self.controller.edit_curve_start(curve_id)
        self.edit_curve_window = CurveEditWindow(curve_id, parent=self)
        self.set_panel_widget(self.edit_curve_window)

    def edit_curve_finish(self):
        self.controller.edit_curve_finish()
        self.set_mode(self.modes.NONE)

    def edit_curve_list_close(self):
        self.set_mode(self.modes.NONE)

    def delete_curve(self, curve_id: str):
        self.controller.delete_curve(curve_id)

    # Notifications from scene handling

    def _add_curve_scene_click_action(self, point: QtCore.QPointF):
        self.add_curve_panel.add_point(point)

    def _add_curve_scene_move_action(self, point: QtCore.QPointF):
        x, y = point.x(), point.y()
        self.add_curve_panel.show_point_pos(x, y)

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
