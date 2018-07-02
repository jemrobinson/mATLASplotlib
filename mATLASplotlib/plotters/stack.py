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
            * **hatchcolour** (*str*) -- which hatch colour to use
            * **label** (*str*) -- label to use when this appears in a legend
            * **outlinewidth** (*str*) -- how wide to draw the outline
        """
        # Construct plotting argument dictionary
        self.plot_args["color"] = kwargs.pop("colour", "black")               # Default colour: black
        if "hatch" in kwargs:
            self.plot_args["hatch"] = kwargs.pop("hatch")                     # Default hatch: do not apply
            self.plot_args["edgecolor"] = kwargs.pop("hatchcolour", "white")  # Default colour: white
        self.plot_args["label"] = kwargs.pop("label", None)                   # Default label: None
        self.plot_args["linewidth"] = kwargs.pop("outlinewidth", 0.0)         # Default linewidth: 0

        # Add any other user-provided arguments
        self.plot_args.update(kwargs)

        # Initialise stack bottom
        if not hasattr(axes, "stack_bottom"):
            axes.stack_bottom = [0] * len(dataset.y_points)

        # Plot with edge colour first if requested
        axes.bar(dataset.x_points, height=dataset.y_points, width=[1.004 * x for x in dataset.x_bin_widths], bottom=axes.stack_bottom, **self.plot_args)

        # Increment stack bottom
        axes.stack_bottom = [increment + previous for increment, previous in zip(dataset.y_points, axes.stack_bottom)]
