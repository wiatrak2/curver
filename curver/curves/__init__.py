from curver.curves.curve import Curve
from curver.curves.polyline import Polyline
from curver.curves.lagrange import Lagrange

types = {
    Polyline.type: Polyline,
    Lagrange.type: Lagrange,
}
