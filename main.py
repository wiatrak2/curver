from PyQt5 import QtWidgets

from curve_editor import CurveEditor

app = QtWidgets.QApplication([])
window = CurveEditor()
window.show()
app.exec_()

