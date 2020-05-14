from PyQt5 import QtWidgets

from curver import CurveEditor

app = QtWidgets.QApplication([])
window = CurveEditor()
window.show()
app.exec_()
