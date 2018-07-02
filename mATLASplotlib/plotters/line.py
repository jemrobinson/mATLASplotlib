"""This module provides the ``Line`` class."""

import logging
import numpy as np
from scipy import interpolate
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class Line(BasePlotter):
    """Plot as a line in the x-y plane

    :Additional plot_style options:
        * `join centres` -- join the centres with straight line segments
        * `smooth` -- draw a smooth line through the points
        * `stepped` -- draw a stepped line graph
    """

    def add_to_axes(self, axes, dataset, **kwargs):
        """Add the chosen dataset to the chosen axes.

        :param axes: which axes to plot this dataset on
        :type axes: matplotlib.axes
        :param dataset: which axes to plot this dataset on
        :type dataset: matplotlib.axes

        :Keyword Arguments:
            * **colour** (*str*) -- which face colour to use
            * **label** (*str*) -- label to use when this appears in a legend
            * **linestyle** (*str*) -- which style (dotted/dashed/solid etc.) to draw the line with
            * **linewidth** (*str*) -- how wide to draw the line
            * **marker** (*str*) -- which marker to use
        """
        # Construct plotting argument dictionary
        self.plot_args["color"] = kwargs.pop("colour", "black")         # Default colour: black
        self.plot_args["label"] = kwargs.pop("label", None)             # Default label: None
        self.plot_args["linestyle"] = kwargs.pop("linestyle", "solid")  # Default linewidth: solid
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 2)        # Default linewidth: 2
        self.plot_args["marker"] = kwargs.pop("marker", None)           # Default marker: dot

        # Add any other user-provided arguments
        self.plot_args.update(kwargs)

        # Set draw style, defaulting to "join centres"
        line_draw_style = "join centres"
        if "smooth" in self.plot_style:
            line_draw_style = "smooth"
        elif "stepped" in self.plot_style:
            line_draw_style = "stepped"

        if line_draw_style == "join centres":
            axes.plot(dataset.x_points, dataset.y_points, **self.plot_args)
        elif line_draw_style == "smooth":
            spline = interpolate.interp1d(dataset.x_points, dataset.y_points, kind="cubic")
            x_spline = np.linspace(min(dataset.x_points), max(dataset.x_points), 10 * len(dataset.x_points))
            y_spline = spline(x_spline)
            axes.plot(x_spline, y_spline, **self.plot_args)
        elif line_draw_style == "stepped":
            axes.plot(dataset.x_all_bin_edges, dataset.y_at_x_bin_edges, drawstyle="steps-pre", **self.plot_args)
