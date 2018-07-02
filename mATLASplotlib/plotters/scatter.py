"""This module provides the ``Scatter`` class."""

import logging
import numpy as np
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class Scatter(BasePlotter):
    """Plot as scattered points in the x-y plane"""

    def __init__(self, plot_style):
        """Initialise plotting properties.

        :param plot_style: which plotting style to use.
        :type plot_style: str

        :Plot_style options:
            * `scatter join centres` -- also draw a line joining the bin centre
            * `scatter xerror` -- also draw error bars in the x-direction
            * `scatter yerror` -- also draw error bars in the y-direction
        """
        super(Scatter, self).__init__(plot_style)
        self.join_centres = "join centres" in plot_style
        self.show_x_errors = "xerror" in plot_style
        self.show_y_errors = "yerror" in plot_style

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        """Add the chosen dataset to the chosen axes.

        :param axes: which axes to plot this dataset on
        :type axes: matplotlib.axes
        :param dataset: which axes to plot this dataset on
        :type dataset: matplotlib.axes

        :Keyword Arguments:
            * **colour** (*str*) -- which face colour to use
            * **label** (*str*) -- label to use when this appears in a legend
            * **linestyle** (*str*) -- which style (dotted/dashed/solid etc.) to draw the line with if `join centers` is specified
            * **linewidth** (*str*) -- how wide to draw the line
            * **marker** (*str*) -- which marker to use
            * **with_error_bar_caps** (*bool*) -- whether to draw caps on the end of the error bars
        """
        # Construct plotting argument dictionary
        self.plot_args["color"] = kwargs.pop("colour", "black")  # Default colour: black
        self.plot_args["label"] = kwargs.pop("label", None)      # Default label: None
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 2)  # Default linewidth: 2
        self.plot_args["marker"] = kwargs.pop("marker", "o")     # Default marker: dot

        # Extract other known arguments from kwargs
        linestyle = kwargs.pop("linestyle", "solid")                   # Default linestyle: solid
        with_error_bar_caps = kwargs.pop("with_error_bar_caps", False)  # Default: False

        # Add any other user-provided arguments
        self.plot_args.update(kwargs)

        # Set whether error bars are shown
        if self.show_x_errors:
            self.plot_args["xerr"] = np.transpose(dataset.x_error_pairs)
        if self.show_y_errors:
            self.plot_args["yerr"] = np.transpose(dataset.y_error_pairs)
        # Get error cap sizes
        if self.show_x_errors or self.show_y_errors:
            self.plot_args["capthick"] = self.plot_args.get("linewidth") if with_error_bar_caps else 0
            self.plot_args["capsize"] = 2 * self.plot_args.get("linewidth") if with_error_bar_caps else 0
        else:
            self.plot_args["markeredgewidth"] = 0  # force error bar cap removal (unnecessary in newer matplotlib versions)

        # Draw points using errorbar
        axes.errorbar(dataset.x_points, dataset.y_points, fmt="", linestyle="None", **self.plot_args)

        # Draw a line joining the points
        if self.join_centres:
            axes.plot(dataset.x_points, dataset.y_points, linestyle=linestyle, **self.plot_args)
