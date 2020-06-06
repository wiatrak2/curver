import json
import logging

import daiquiri
from PyQt5 import QtCore, QtWidgets

from curver import CurveController, curves, panels, utils, widgets
from curver.ui.main_ui import Ui_Curver

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)


class CurveEditor(QtWidgets.QMainWindow):
    modes = utils.ControllerModes

    def __init__(self):
        super().__init__()
        self.ui = Ui_Curver()
        self.ui.setupUi(self)
        self._setup_editor_ui()

        self.controller = CurveController(self.scene, main_ui=self)

        self.add_curve_panel = panels.AddCurvePanel(self)

        self.mode = self.modes.NONE
        self._update_ui()

        self.current_curve_type = None

        self.edit_curves_list = None
        self.edit_curve_window = None

    @property
    def scene(self) -> widgets.CurverGraphicsScene:
        return self.ui.plane.scene()

    @property
    def panel_widget(self) -> QtWidgets.QWidget:
        return self.ui.panelLayout.itemAt(0).widget()

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

    def _create_canvas(
        self, width=700, height=500, line_len=1000
    ) -> QtWidgets.QGraphicsScene:
        scene = widgets.CurverGraphicsScene(width, height, line_len, parent=self)
        return scene

    def _connect_actions(self):
        self.ui.actionImportCurve.triggered.connect(self._import_curve_action)
        self.ui.actionExportScene.triggered.connect(self._export_scene_action)

    def _update_ui(self):
        if self.mode == self.modes.NONE:
            self.set_panel_widget(self.add_curve_panel)

    # Button actions

    def _import_curve_action(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, "Import curve", filter="*.json"
        )
        self._import_curve(filename[0])

    def _import_curve(self, filename):
        logger.info(f"Importing curve from {filename}.")
        try:
            with open(filename, "r") as f:
                curves_list = json.load(f)
        except:
            logger.warning(f"Could not load curve from {filename}.")
            return
        for curve_info in curves_list:
            curve_cls = curves.types[curve_info.get("type", curves.Curve)]
            curve_id = curve_info.get("id", "")
            curve_points = [
                QtCore.QPointF(x, y) for (x, y) in curve_info.get("points", [])
            ]
            curve_weights = None
            if curve_cls.weighted:
                curve_weights = curve_info.get("weights")
            self.controller.create_curve(
                curve_id, curve_cls, curve_points, weights=curve_weights
            )
            logger.info(
                f"Curve {curve_id} of type {curve_cls.type} with {len(curve_points)} points successfully imported."
            )

    def _export_scene_action(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save", "scene.json", ".json"
        )
        self._export_scene_to_file(filename[0])

    def _export_scene_to_file(self, filename: str):
        all_curves = self.controller.curve_ids()
        curves_dict = [
            self.controller.serialize_curve(curve_id) for curve_id in all_curves
        ]
        with open(filename, "w") as f:
            json.dump(curves_dict, f)

    def edit_curve_start(self, curve_id: str):
        self.set_mode(self.modes.EDIT)
        self.controller.edit_curve_start(curve_id)
        self.edit_curve_window = panels.CurveEditWindow(curve_id, parent=self)
        self.set_panel_widget(self.edit_curve_window)

    def edit_curve_finish(self):
        self.controller.edit_curve_finish()
        self.set_mode(self.modes.NONE)

    def edit_curve_list_close(self):
        self.set_mode(self.modes.NONE)

    def delete_curve(self, curve_id: str):
        self.controller.delete_curve(curve_id)

    # Notifications from scene handling

    def notify_scene_pos(self, point: QtCore.QPointF):
        if self.controller.mode == self.controller.modes.NONE:
            return
        self.panel_widget.notify_scene_pos(point)

    def mouse_click_action(self, point: QtCore.QPointF):
        if self.controller.mode == self.controller.modes.NONE:
            return
        self.panel_widget.mouse_click_action(point)
