from PyQt5 import QtWidgets

from curver import CurveEditor

def main():
    app = QtWidgets.QApplication([])
    window = CurveEditor()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
