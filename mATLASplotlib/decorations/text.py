"""This module provides the draw_text convenience function."""


def draw_text(text, x, y, axes, fontsize=16, **kwargs):
    """Draw arbitrary text strings at (x, y) on the chosen axes."""
    interpreted_kwargs = {"ha": kwargs["ha"], "va": kwargs["va"]}
    interpreted_kwargs["color"] = kwargs.pop("colour", "black")
    interpreted_kwargs["transform"] = {"data": axes.transData, "axes": axes.transAxes}[kwargs.pop("coordinates", "axes")]
    axes.text(x, y, text, fontsize=fontsize, **interpreted_kwargs)
