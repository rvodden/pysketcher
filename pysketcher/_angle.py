import numpy as np


class Angle(float):
    r"""A representation of a 2-Dimensional Angle.

    An ``Angle`` is a float which is limited in value to between :math:`\pi`
    and :math:`-\pi`. Values outside of this range have :math:`2\pi` either added
    or subtracted repeatedly until they are within this bound.

    Args:
        value: The value of the angle to create.

    Examples:
        >>> Angle(1.0)
        Angle(1.0)

        >>> Angle(np.pi / 2)
        Angle(1.5707963267948966)

        >>> Angle(123)
        Angle(-2.6637061435917246)

        >>> Angle(2 * np.pi)
        Angle(0.0)
    """

    def __new__(cls, value: float) -> "Angle":
        """Creates a new Angle."""
        value = cls._normalize(value)
        return super(cls, cls).__new__(cls, value)

    @staticmethod
    def _normalize(value: float):
        retval = value - 2 * np.pi * (np.ceil((value + np.pi) / (2 * np.pi)) - 1)
        # TODO: this step should not be necessary - what is wrong with the above?
        if not (-np.pi < retval <= np.pi):
            retval = Angle._normalize(retval)
        return retval

    def __add__(self, other: float) -> "Angle":
        """Returns the sum of this ``Angle`` with the provided ``Angle``."""
        res = super(self.__class__, self).__add__(other)
        return self.__class__(res)

    def __sub__(self, other: float) -> "Angle":
        """Returns the difference between this ``Angle`` and the provided ``Angle``."""
        res = super(self.__class__, self).__sub__(other)
        return self.__class__(res)

    def __mul__(self, other: float) -> "Angle":
        """Scales the ``Angle`` by a factor of the provided value."""
        res = super(self.__class__, self).__mul__(other)
        return self.__class__(res)

    def __truediv__(self, other: float) -> "Angle":
        """Divides the ``Angle`` by the provided factor."""
        res = super(self.__class__, self).__truediv__(other)
        return self.__class__(res)

    def __str__(self: float) -> str:
        """Provides a string rendition of the value of the ``Angle``."""
        return f"{float(self)}"

    def __repr__(self: float) -> str:
        """Provides a string rendition of the value of the ``Angle`` and class."""
        return f"Angle({float(self)})"
