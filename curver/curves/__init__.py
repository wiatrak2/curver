from curver.curves.curve import Curve
from curver.curves.base_curve import BaseCurve
from curver.curves.polyline import Polyline
from curver.curves.lagrange import Lagrange
from curver.curves.bezier import Bezier
from curver.curves.rational_bezier import RationalBezier
from curver.curves.cubic_spline import CubicSpline


types = {
    Polyline.type: Polyline,
    Lagrange.type: Lagrange,
    Bezier.type: Bezier,
    RationalBezier.type: RationalBezier,
    CubicSpline.type: CubicSpline,
}
