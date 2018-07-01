"""This module provides the ``Stack`` class."""

import logging
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class Stack(BasePlotter):
    """Plot as part of a vertically stacked histogram."""

    def add_to_axes(self, axes, dataset, **kwargs):
        """Add the chosen dataset to the chosen axes.

        :param axes: which axes to plot this dataset on
        :type axes: matplotlib.axes
        :param dataset: which axes to plot this dataset on
        :type dataset: matplotlib.axes

        :Keyword Arguments:
            * **colour** (*str*) -- which face colour to use
            * **hatch** (*str*) -- set hatch pattern
            * **line_colour** (*float*) -- which colour to use for the main line and for hatches
            * **edgecolour** (*float*) -- which colour to use for the outline
            * **label** (*str*) -- label to use when this appears in a legend
        """
        logger.debug("Adding dataset to axes as stack")
        # Interpret arguments
        self.plot_args["color"] = kwargs.pop("colour", "black")                          # Default colour: black
        self.plot_args["label"] = kwargs.pop("label", None)                              # Default label: None
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 0.0)                       # Default linewidth: 0
        self.plot_args["edgecolor"] = kwargs.pop("edgecolour", self.plot_args["color"])  # Default edgecolour: match fill colour
        if kwargs.get("hatch", None) is not None:
            self.plot_args["hatch"] = kwargs.pop("hatch")                                # Default hatch: do not apply

        if not hasattr(axes, "stack_bottom"):
            axes.stack_bottom = [0] * len(dataset.y_points)
        axes.bar(dataset.x_points, height=dataset.y_points, width=dataset.x_bin_widths, bottom=axes.stack_bottom, **self.plot_args)
        axes.stack_bottom = [increment + previous for increment, previous in zip(dataset.y_points, axes.stack_bottom)]
