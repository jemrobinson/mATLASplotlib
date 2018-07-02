"""This module provides the ``get_plotter()`` convenience function."""
from functools import partial


def force_extra_ticks(x_ticks_extra):
    """Implement user-defined tick positions.

    :param x: tick value.
    :type x: float
    :param pos: position.
    :type pos: float
    :return: formatted tick position string
    :rtype: str
    """
    def inner(x, pos, x_ticks_extra):
        del pos  # this function signature is required by FuncFormatter
        if any(int(x) == elem for elem in x_ticks_extra):
            return "{0:.0f}".format(x)
        return ""
    return partial(inner, x_ticks_extra=x_ticks_extra)


def force_ndp(nplaces):
    """Force rounding for all labels.

    :param nplaces: how many decimal places to use.
    :type nplaces: int
    :return: tick formatter
    :rtype: function
    """
    def inner(x, pos, nplaces):
        del pos  # this function signature is required by FuncFormatter
        return "{0:.{1}f}".format(x, nplaces)
    return partial(inner, nplaces=nplaces)
