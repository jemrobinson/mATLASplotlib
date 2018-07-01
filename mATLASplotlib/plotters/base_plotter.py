"""This module provides the ``BasePlotter`` class."""

import logging

logger = logging.getLogger("mATLASplotlib.plotters")


class BasePlotter(object):
    """Base class for plot formatting."""

    def __init__(self, plot_style):
        """Initialise common plotting properties.

        :param plot_style: which plotting style to use. Consists of plot style name, plus any additional options available in the child class.
        :type plot_style: str
        """
        self.plot_style = plot_style
        self.plot_args = {}

    def add_to_axes(self, axes, dataset, **kwargs):
        """Add the chosen dataset to the chosen axes. Delegated to child classes.

        :param axes: which axes to plot this dataset on
        :type axes: matplotlib.axes
        :param dataset: dataset to plot
        :type dataset: Dataset
        """
        raise NotImplementedError("add_to_axes not defined by {0}".format(type(self)))
