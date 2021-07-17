import numpy as np

from pysketcher._angle import Angle
from pysketcher._curve import Curve
from pysketcher._point import Point


class Arc(Curve):
    """A representation of a continuous connected subset of a circle.

    Args:
        center: The center of the Arc.
        radius: The radius of the Arc.
        start_angle: The angle from the +ve horizontal where the Arc should start.
        arc_angle: The angle (from the start_angle) where the Arc should end.
        resolution: The number of points in the Arc.

    Examples:
        >>> arc = ps.Arc(ps.Point(0.0, 0.0), 1.0, Angle(0.0), Angle(np.pi / 2))
        >>> fig = ps.Figure(-0.5, 1.5, -0.5, 1.5, backend=MatplotlibBackend)
        >>> fig.add(arc)
        >>> fig.save("pysketcher/images/arc.png")

    .. figure:: images/arc.png
        :alt: An example of an Arc.
        :figclass: align-center

        An example of an ``Arc``.
    """

    _center: Point
    _radius: float
    _start_angle: Angle
    _arc_angle: Angle
    _resolution: int

    def __init__(
        self,
        center: Point,
        radius: float,
        start_angle: Angle,
        arc_angle: Angle,
        resolution: int = 180,
    ):
        # Must record some parameters for __call__
        self._center = center
        self._radius = radius
        self._start_angle = Angle(start_angle)
        self._arc_angle = Angle(arc_angle)
        self._resolution = resolution

        if self._arc_angle == 0.0:
            # assume a full circle
            ts = np.linspace(0.0, 2.0 * np.pi, resolution + 1)
        else:
            ts = np.linspace(0.0, self._arc_angle, resolution + 1)

        points = [self(t) for t in ts]
        super().__init__(points)

    def __call__(self, theta: Angle) -> Point:
        """Provides a point on the arc ``theta`` of the way around.

        Args:
            theta: The angle from the ``start_angle`` from which the point should
                be taken.

        Returns:
            the point ``theta`` of the way around the arc.

        Raises:
            ValueError: if ``theta`` is beyond the bounds of the arc.
        """
        if 0.0 < self._arc_angle < theta or theta < self._arc_angle < 0.0:
            raise ValueError(
                f"Theta ({theta}) is outside the bounds "
                "of the arc (0.0 , {self._arc_angle})"
            )

        iota = Angle(self.start_angle + theta)
        ret_point = Point(
            self.center.x + self.radius * np.cos(iota),
            self.center.y + self.radius * np.sin(iota),
        )
        return ret_point

    @property
    def start_angle(self) -> Angle:
        """The angle from the +ve horizontal from where the arc starts."""
        return self._start_angle

    @property
    def arc_angle(self) -> Angle:
        """The angle from the ``start_angle`` to which the arc ends."""
        return self._arc_angle

    @property
    def end_angle(self) -> Angle:
        """The angle from the +ve horizontal to which the arc ends."""
        return self._start_angle + self._arc_angle

    @property
    def radius(self) -> float:
        """The radius of the arc."""
        return self._radius

    @property
    def center(self) -> Point:
        """The center of the arc."""
        return self._center

    @property
    def start(self) -> Point:
        """The point at which the arc starts."""
        return self(0.0)

    @property
    def end(self) -> Point:
        """The point at which the arc ends."""
        return self(self.arc_angle)

    @property
    def mid(self) -> Point:
        """The middle of the arc."""
        return self(self.arc_angle / 2)

    def translate(self, vec: Point) -> "Arc":
        """Translates the arc by the specified vector.

        Args:
            vec: The vector through which the arc should be translated.

        Returns:
            A copy of the arc which has been translated by ``vec``.
        """
        arc = Arc(
            self._center + vec,
            self._radius,
            self._start_angle,
            self._arc_angle,
            self._resolution,
        )
        arc.style = self.style
        return arc
