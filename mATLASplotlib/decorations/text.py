"""This module provides the ``draw_text`` convenience function."""


def draw_text(text, x, y, axes, ha, va, fontsize=16, **kwargs):
    """Draw arbitrary text strings at (x, y) on the chosen axes.

    :param x: x-position of text
    :type x: float
    :param y: y-position of text
    :type y: float
    :param axes: axes to plot on
    :type axes: str
    :param fontsize: fontsize of legend contents
    :type fontsize: float
    :param ha: horizontal alignment
    :type ha: str
    :param va: vertical aligment
    :type va: str

    :Keyword Arguments:
        * **colour** (*str*) -- set text colour
        * **transform** (*str*) -- use data or axes coordinates
    """
    interpreted_kwargs = {"ha": ha, "va": va}
    interpreted_kwargs["color"] = kwargs.pop("colour", "black")
    interpreted_kwargs["transform"] = {"data": axes.transData, "axes": axes.transAxes}[kwargs.pop("coordinates", "axes")]
    axes.text(x, y, text, fontsize=fontsize, **interpreted_kwargs)
