#! /usr/bin/env python


class Text(object):
    """Document here."""

    def __init__(self, text):
        """Constructor."""
        self.text = text
        self.default_fontsize = 16

    def draw(self, x, y, axes, ha, va, fontsize):
        """Document here."""
        axes.text(x, y, self.text, fontsize=[fontsize, self.default_fontsize][fontsize is None], ha=ha, va=va, transform=axes.transAxes)
