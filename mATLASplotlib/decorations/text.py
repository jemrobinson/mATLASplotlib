"""This module provides the ``draw_text`` convenience function."""


# def draw_text(text, x, y, axes, ha, va, fontsize=16, **kwargs):
def draw_text(text, axes, loc, align, fontsize=16, **kwargs):
    """Draw arbitrary text strings at (x, y) on the chosen axes.

    :param text: text to draw
    :type text: str
    :param axes: axes to plot on
    :type axes: str
    :param loc: x and y position of text
    :type loc: tuple(float)
    :param align: horizontal and vertical alignment of text
    :type align: tuple(str)
    :param fontsize: fontsize of legend contents
    :type fontsize: float

    :Keyword Arguments:
        * **colour** (*str*) -- set text colour
        * **transform** (*str*) -- use data or axes coordinates
    """
    interpreted_kwargs = {"ha": align[0], "va": align[1]}
    interpreted_kwargs["color"] = kwargs.pop("colour", "black")
    interpreted_kwargs["transform"] = {"data": axes.transData, "axes": axes.transAxes}[kwargs.pop("coordinates", "axes")]
    axes.text(loc[0], loc[1], text, fontsize=fontsize, **interpreted_kwargs)
