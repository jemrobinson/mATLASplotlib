import logging
from matplotlib import __version__ as mpl_version
import numpy as np

logger = logging.getLogger("mATLASplotlib.plotters")

class Scatter(object):
    """Plot as points in the x-y plane"""
    def __init__(self, plot_style):
        self.show_x_errors = "xerror" in plot_style
        self.show_y_errors = "yerror" in plot_style

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        # Construct plotting arguments
        plot_args = {}
        plot_args["color"] = kwargs.pop("colour", "black")        # Default colour: black
        plot_args["label"] = kwargs.pop("label", None)            # Default label: None
        plot_args["linewidth"] = kwargs.pop("linewidth", 2)       # Default linewidth: 2
        plot_args["marker"] = kwargs.pop("marker", "o")           # Default marker: dot
        # Set whether error bars are shown
        if self.show_x_errors:
            plot_args["xerr"] = np.transpose(dataset.x_error_pairs)
        if self.show_y_errors:
            plot_args["yerr"] = np.transpose(dataset.y_error_pairs)
        # Get error cap sizes
        if mpl_version > "1.4.0":
            with_error_bar_caps = kwargs.pop("with_error_bar_caps", False)
            plot_args["capthick"] = [0, plot_args.get("linewidth")][with_error_bar_caps]
            plot_args["capsize"] = [0, 2 * plot_args.get("linewidth")][with_error_bar_caps]
        else:
            print "Matplotlib version {} is too old to allow error bar caps".format(mpl_version)

        # Draw points using errorbar
        (joining_line, caplines, error_line) = axes.errorbar(dataset.x_points, dataset.y_points, fmt="", markeredgewidth=0, linestyle='None', **plot_args)

        # Draw a line joining the points
        if "join_centres" in kwargs and kwargs["join_centres"]:
            # Set custom dash styling
            plot_args["linestyle"] = kwargs.pop("linestyle", "solid") # Default linestyle: solid
            if plot_args["linestyle"] is "dashed":
                plot_args["dashes"] = (3 * plot_args["linewidth"], 1 * plot_args["linewidth"])
            if plot_args["linestyle"] is "dotted":
                plot_args["dashes"] = (1 * plot_args["linewidth"], 1 * plot_args["linewidth"])
            if plot_args["linestyle"] is "dashdot":
                plot_args["dashes"] = (2 * plot_args["linewidth"], 1 * plot_args["linewidth"], 1 * plot_args["linewidth"], 1 * plot_args["linewidth"])
            axes.plot(dataset.x_points, dataset.y_points, **plot_args)
