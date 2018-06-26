"""This module provides the BinnedBand class."""

import logging
import numpy as np
from matplotlib.patches import Rectangle, Ellipse
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class BinnedBand(BasePlotter):
    """Plot as binned band in the x-y plane"""
    # Add to canvas

    def add_to_axes(self, axes, dataset, **kwargs):
        # Construct plotting arguments
        self.plot_args["facecolor"] = kwargs.pop("colour", "black")            # Default colour: black
        self.plot_args["edgecolor"] = kwargs.pop("background_colour", "white")  # Default colour: white
        line_colour = kwargs.pop("line_colour", "white")
        self.plot_args["hatch"] = kwargs.pop("hatch", None)                    # Default hatch: None
        self.plot_args["alpha"] = kwargs.pop("alpha", None)                    # Default alpha: None
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 0)               # Default linewidth: 2
        # Add any other user-provided arguments
        plot_label = kwargs.pop("label", None)                                 # Default label: None
        self.plot_args.update(kwargs)

        if "central line" in self.plot_style:
            axes.errorbar(dataset.x_points, dataset.y_points, fmt="", markeredgewidth=0, linestyle="None", color=line_colour, xerr=np.transpose(dataset.x_error_pairs))

        if plot_label is None:
            axes.fill_between(dataset.band_edges_x, dataset.band_edges_y_low, dataset.band_edges_y_high, **self.plot_args)
        else:
            axes.fill_between(dataset.band_edges_x, dataset.band_edges_y_low, dataset.band_edges_y_high, **self.plot_args)

            if "central line" in self.plot_style:
                proxy_artist = Ellipse((0, 0), 0, 0, axes=axes, label=plot_label, facecolor=self.plot_args["facecolor"], edgecolor=line_colour)
                axes.add_patch(proxy_artist)
            else:
                proxy_artist = Rectangle((0, 0), 0, 0, axes=axes, label=plot_label, **self.plot_args)
                axes.add_patch(proxy_artist)
