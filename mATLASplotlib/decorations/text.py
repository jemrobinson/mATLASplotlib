#! /usr/bin/env python


class Text(object):
    """Document here."""

    def __init__(self, text):
        """Constructor."""
        self.text = text
        self.default_fontsize = 16

    def draw(self, x, y, axes, ha, va, **kwargs):
        """Document here."""
        interpreted_kwargs = {}
        interpreted_kwargs["fontsize"] = kwargs.pop("fontsize", self.default_fontsize)
        interpreted_kwargs["color"] = kwargs.pop("colour", "black")
        interpreted_kwargs["transform"] = {"data": axes.transData, "axes": axes.transAxes}[kwargs.pop("coordinates", "axes")]
        axes.text(x, y, self.text, ha=ha, va=va, **interpreted_kwargs)
