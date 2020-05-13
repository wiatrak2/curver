from PyQt5 import uic, QtWidgets, QtGui, QtCore

from curver import curves, widgets, utils, curve_controller
from curver.ui.add_point_panel_ui import Ui_addCurveWidget
from curver.curve_edit_list import CurvesListWindow

class addCurvePanel(QtWidgets.QWidget):
    modes = utils.ControllerModes

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        assert parent.controller, "Parent of CurvesListWindow must have controller"
        self.controller: CurveController = parent.controller
        self._parent = parent

        self.mode = self.modes.NONE
        self.current_curve_type = None

        self.ui = Ui_addCurveWidget()
        self.ui.setupUi(self)
        self._setup_ui()
        self._connect_actions()

    def set_mode(self, new_mode):
        self.mode = new_mode
        self._update_ui()

    def _setup_ui(self):
        self.ui.setCurveType.addItems(curves.types.keys())
        self._update_ui()

    def _update_ui(self):
        self.ui.addPointBox.setVisible(self.mode == self.modes.ADD)
        self.ui.weightBox.setVisible(self.mode == self.modes.ADD and self.current_curve_type.weighted)
        self.ui.weightVal.setText("1.0")

    def _connect_actions(self):
        self.ui.addCurveButton.clicked.connect(self.add_curve_button_action)
        self.ui.addPointButton.clicked.connect(self.add_point_button_action)
        self.ui.undoAddPointButton.clicked.connect(self.undo_add_point_button_action)
        self.ui.cancelAddCurveButton.clicked.connect(
            self.cancel_add_curve_button_action
        )
        self.ui.saveCurveButton.clicked.connect(self.save_curve_button_action)
        self.ui.editCurveButton.clicked.connect(self.edit_curve_button_action)

    def add_curve_button_action(self):
        print(self.mode)
        if self.mode == self.modes.NONE:
            curve_type = self.ui.setCurveType.currentText()
            curve_cls = curves.types[curve_type]
            curve_id = f"{curve_type}_{len(self.controller.curves)+1}"  # TODO: unique names, even after removing curve
            self.ui.curveName.setText(curve_id)
            self.current_curve_type = curve_cls
            self.controller.create_curve_start(curve_id, curve_cls)
            self.set_mode(self.modes.ADD)

    def add_point_button_action(self):
        self.add_point()

    def undo_add_point_button_action(self):
        self.controller.delete_point_idx(-1)

    def cancel_add_curve_button_action(self):
        self.controller.delete_curve()
        self.ui.addPointBox.setHidden(True)
        self.set_mode(self.modes.NONE)

    def save_curve_button_action(self):
        curve_id = self.ui.curveName.text()
        curve_id_success = self.controller.rename_curve(curve_id)
        if not curve_id_success:
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setText("Curve with given name already exists")
            msg_box.exec_()
            return

        self.controller.create_curve_finish()
        self.current_curve_type = None
        self.set_mode(self.modes.NONE)

    def edit_curve_button_action(self):
        if self.mode == self.modes.NONE:
            self.edit_curves_list = CurvesListWindow(self._parent, self.controller.curves)
            self.controller.set_panel_widget(self.edit_curves_list)

    def add_point(self, point: QtCore.QPointF = None):
        if point is None:
            x, y = float(self.ui.xPos.text()), float(self.ui.yPos.text())
            point = QtCore.QPointF(x, y)
        weight = None
        if self.ui.weightBox.isVisible():
            weight = float(self.ui.weightVal.text()) or 1.
            self.ui.weightVal.setText("1.0")
        self.controller.add_point(point, weight=weight)

    def show_point_pos(self, x, y):
        self.ui.xPos.setText(str(int(x)))
        self.ui.yPos.setText(str(int(y)))
