"""This module provides the Scatter class."""

import logging
import numpy as np
from matplotlib import __version__ as mpl_version
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class Scatter(BasePlotter):
    """Plot as points in the x-y plane"""

    def __init__(self, plot_style):
        """Constructor."""
        super(Scatter, self).__init__(plot_style)
        self.show_x_errors = "xerror" in plot_style
        self.show_y_errors = "yerror" in plot_style
        self.join_centres = "join centres" in plot_style

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        # Construct plotting arguments
        self.plot_args["color"] = kwargs.pop("colour", "black")        # Default colour: black
        self.plot_args["label"] = kwargs.pop("label", None)            # Default label: None
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 2)       # Default linewidth: 2
        self.plot_args["marker"] = kwargs.pop("marker", "o")           # Default marker: dot
        # Add any other user-provided arguments
        self.plot_args.update(kwargs)
        # Set whether error bars are shown
        if self.show_x_errors:
            self.plot_args["xerr"] = np.transpose(dataset.x_error_pairs)
        if self.show_y_errors:
            self.plot_args["yerr"] = np.transpose(dataset.y_error_pairs)
        # Get error cap sizes
        if self.show_x_errors or self.show_y_errors:
            if mpl_version > "1.4.0":
                with_error_bar_caps = kwargs.pop("with_error_bar_caps", False)
                self.plot_args["capthick"] = self.plot_args.get("linewidth") if with_error_bar_caps else 0
                self.plot_args["capsize"] = 2 * self.plot_args.get("linewidth") if with_error_bar_caps else 0
            else:
                logger.warning("Matplotlib version {} is too old to allow error bar caps".format(mpl_version))

        # Draw points using errorbar
        axes.errorbar(dataset.x_points, dataset.y_points, fmt="", markeredgewidth=0, linestyle="None", **self.plot_args)

        # Draw a line joining the points
        self.plot_args["linestyle"] = kwargs.pop("linestyle", "solid")  # Default linestyle: solid
        if self.join_centres or kwargs.pop("join_centres", False):
            # Set custom dash styling
            if self.plot_args["linestyle"] == "dashed":
                self.plot_args["dashes"] = (3 * self.plot_args["linewidth"], 1 * self.plot_args["linewidth"])
            if self.plot_args["linestyle"] == "dotted":
                self.plot_args["dashes"] = (1 * self.plot_args["linewidth"], 1 * self.plot_args["linewidth"])
            if self.plot_args["linestyle"] == "dashdot":
                self.plot_args["dashes"] = (2 * self.plot_args["linewidth"], 1 * self.plot_args["linewidth"], 1 * self.plot_args["linewidth"], 1 * self.plot_args["linewidth"])
            axes.plot(dataset.x_points, dataset.y_points, **self.plot_args)
