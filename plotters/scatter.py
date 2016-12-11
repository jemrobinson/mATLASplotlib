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

        # Draw using matplotlib
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


    #     if plot_style.startswith("point"):
    #         if "xerror" in plot_style:
    #             kwargs["xerr"] = np.transpose(self.x_error_pairs)
    #         if "yerror" in plot_style:
    #             kwargs["yerr"] = np.transpose(self.y_error_pairs)
    #         # Get error cap sizes
    #         if mpl_version > "1.4.0":
    #             with_error_bar_caps = kwargs.pop("with_error_bar_caps", False)
    #             kwargs["capthick"] = [0, kwargs.get("linewidth")][with_error_bar_caps]
    #             kwargs["capsize"] = [0, 2 * kwargs.get("linewidth")][with_error_bar_caps]
    #         else:
    #             print "Matplotlib version {} is too old to allow error bar caps".format(mpl_version)
    #         # Disable linestyle
    #         dashes = kwargs.pop("linestyle", "solid")
    #         kwargs["linestyle"] = "None"
    #         if "dashes" in kwargs:
    #             kwargs.pop("dashes")
    #         (joining_line, caplines, error_line) = axes.errorbar(self.x_points, self.y_points, fmt="", markeredgewidth=0, **kwargs)
    #         try:
    #             error_line[0].set_linestyle(dashes)
    #         except IndexError:
    #             pass
    #         if "capsize" in kwargs:
    #             [capline.set_markeredgewidth(kwargs["capsize"]) for capline in caplines]
    #
    #     elif "bar" in plot_style:
    #         if "filled" in plot_style:
    #             if hatch != None:
    #                 kwargs["hatch"] = hatch
    #         if "stack" in plot_style:
    #             if not hasattr(axes, "stack_bottom"):
    #                 axes.stack_bottom = [0] * len(self.y_points)
    #             axes.bar(self.x_bin_low_edges, height=self.y_points, width=self.x_bin_widths, edgecolor=colour_secondary, bottom=axes.stack_bottom, **kwargs)
    #             axes.stack_bottom = [additional + old for additional, old in zip(self.y_points, axes.stack_bottom)]
    #         else:
    #             axes.bar(self.x_bin_low_edges, height=self.y_points, width=self.x_bin_widths, edgecolor=colour_secondary, **kwargs)
    #
    #     elif plot_style == "join centres":
    #         axes.plot(self.x_points, self.y_points, **kwargs)
    #
    #     elif plot_style == "stepped line":
    #         axes.plot(self.x_all_bin_edges, self.y_at_x_bin_edges, drawstyle="steps", **kwargs)
    #
    #     else:
    #         raise NotImplementedError("Style "{}" not recognised by {}.".format(plot_style, type(self)))
