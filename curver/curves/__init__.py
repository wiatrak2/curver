from curver.curves.curve import Curve
from curver.curves.polyline import Polyline
from curver.curves.lagrange import Lagrange
from curver.curves.bezier import Bezier

types = {
    Polyline.type: Polyline,
    Lagrange.type: Lagrange,
    Bezier.type: Bezier,
}
