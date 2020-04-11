from PyQt5 import QtWidgets

def set_widget_geometry(child: QtWidgets.QWidget, parent: QtWidgets.QWidget, mode="left"):
    c_w, c_h = child.width(), child.height()
    p_w, p_h = parent.width(), parent.height()
    p_x, p_y = parent.geometry().x(), parent.geometry().y()
    if mode == "left":
        offset = (p_h - c_h) / 2
        child.setGeometry(p_x - c_w, p_y + offset, c_w, c_h)
    elif mode == "right":
        pass
    elif mode == "top":
        pass
    elif mode == "bottom":
        pass
    else:
        child.setGeometry(p_x, p_y, c_w, c_h)
