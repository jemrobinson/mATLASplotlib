"""This module provides the BasePlotter class."""

import logging

logger = logging.getLogger("mATLASplotlib.plotters")


class BasePlotter(object):
    """Base class for plot formatting."""

    def __init__(self, plot_style):
        """Constructor."""
        self.plot_style = plot_style
        self.plot_args = {}

    def add_to_axes(self, axes, dataset, **kwargs):
        """Document here."""
        raise NotImplementedError("add_to_axes not defined by {0}".format(type(self)))
