from base_plotter import BasePlotter
from matplotlib import __version__ as mpl_version
import logging
import numpy as np

logger = logging.getLogger("mATLASplotlib.plotters")

class Scatter(BasePlotter):
    """Plot as points in the x-y plane"""
    def __init__(self, plot_style):
        """Constructor."""
        super(Scatter, self).__init__(plot_style)
        self.show_x_errors = "xerror" in plot_style
        self.show_y_errors = "yerror" in plot_style

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
        if mpl_version > "1.4.0":
            with_error_bar_caps = kwargs.pop("with_error_bar_caps", False)
            self.plot_args["capthick"] = [0, self.plot_args.get("linewidth")][with_error_bar_caps]
            self.plot_args["capsize"] = [0, 2 * self.plot_args.get("linewidth")][with_error_bar_caps]
        else:
            print "Matplotlib version {} is too old to allow error bar caps".format(mpl_version)

        # Draw points using errorbar
        (joining_line, caplines, error_line) = axes.errorbar(dataset.x_points, dataset.y_points, fmt="", markeredgewidth=0, linestyle="None", **self.plot_args)
        self.plot_args["linestyle"] = kwargs.pop("linestyle", "solid") # Default linestyle: solid

        # Draw a line joining the points
        if "join_centres" in kwargs and kwargs["join_centres"]:
            # Set custom dash styling
            if self.plot_args["linestyle"] is "dashed":
                self.plot_args["dashes"] = (3 * self.plot_args["linewidth"], 1 * self.plot_args["linewidth"])
            if self.plot_args["linestyle"] is "dotted":
                self.plot_args["dashes"] = (1 * self.plot_args["linewidth"], 1 * self.plot_args["linewidth"])
            if self.plot_args["linestyle"] is "dashdot":
                self.plot_args["dashes"] = (2 * self.plot_args["linewidth"], 1 * self.plot_args["linewidth"], 1 * self.plot_args["linewidth"], 1 * plot_args["linewidth"])
            axes.plot(dataset.x_points, dataset.y_points, **plot_args)
