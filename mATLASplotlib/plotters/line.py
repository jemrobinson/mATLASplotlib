"""This module provides the Line class."""

import logging
import numpy as np
from scipy import interpolate
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class Line(BasePlotter):
    """Plot as points in the x-y plane"""
    # Add to canvas

    def add_to_axes(self, axes, dataset, **kwargs):
        # Construct plotting arguments
        self.plot_args["color"] = kwargs.pop("colour", "black")         # Default colour: black
        self.plot_args["label"] = kwargs.pop("label", None)             # Default label: None
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 2)        # Default linewidth: 2
        self.plot_args["marker"] = kwargs.pop("marker", None)           # Default marker: dot
        self.plot_args["linestyle"] = kwargs.pop("linestyle", "solid")  # Default linewidth: solid
        # Add any other user-provided arguments
        self.plot_args.update(kwargs)

        if "stepped" in self.plot_style:
            axes.plot(dataset.x_all_bin_edges, dataset.y_at_x_bin_edges, drawstyle="steps-pre", **self.plot_args)

        if "join centres" in self.plot_style:
            axes.plot(dataset.x_points, dataset.y_points, **self.plot_args)

        if "smooth" in self.plot_style:
            spline = interpolate.interp1d(dataset.x_all_bin_edges, dataset.y_at_x_bin_edges)  # , kind="cubic")
            x_spline = np.linspace(min(dataset.x_all_bin_edges), max(dataset.x_all_bin_edges), 1 * len(dataset.x_all_bin_edges))
            y_spline = spline(x_spline)
            axes.plot(x_spline, y_spline, **self.plot_args)
