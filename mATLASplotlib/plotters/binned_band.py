"""This module provides the ``BinnedBand`` class."""

import logging
import numpy as np
from matplotlib.patches import Rectangle, Ellipse
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class BinnedBand(BasePlotter):
    """Plot as binned band in the x-y plane.

    :Additional plot_style options:
        * `central line` -- also draw a horizontal line at the vertical centre of each bin
        * `central line stepped` -- as for `central line` but also join these vertically at the edge of each bin
    """

    def add_to_axes(self, axes, dataset, **kwargs):
        """Add the chosen dataset to the chosen axes.

        :param axes: which axes to plot this dataset on
        :type axes: matplotlib.axes
        :param dataset: which axes to plot this dataset on
        :type dataset: matplotlib.axes

        :Keyword Arguments:
            * **alpha** (*float*) -- set alpha transparency
            * **colour** (*str*) -- which face colour to use
            * **hatch** (*str*) -- set hatch pattern
            * **hatchcolour** (*str*) -- which hatch colour to use
            * **label** (*str*) -- label to use when this appears in a legend
            * **linecolour** (*float*) -- which colour to use for the main line and for hatches
            * **linewidth** (*str*) -- how wide to draw the line
        """
        # Construct plotting argument dictionary
        self.plot_args["alpha"] = kwargs.pop("alpha", None)          # Default alpha: None
        self.plot_args["facecolor"] = kwargs.pop("colour", "black")  # Default colour: black
        self.plot_args["hatch"] = kwargs.pop("hatch", None)          # Default hatch: None

        # Extract other known arguments from kwargs
        hatch_colour = kwargs.pop("hatchcolour", "white")            # Default colour: white
        line_colour = kwargs.pop("linecolour", "white")              # Default colour: white
        line_style = kwargs.pop("linestyle", None)                   # Default style: None
        line_width = kwargs.pop("linewidth", 2)                      # Default linewidth: 2
        plot_label = kwargs.pop("label", None)                       # Default label: None

        # Add any other user-provided arguments
        self.plot_args.update(kwargs)

        # Plot the central line
        if "central line" in self.plot_style:
            if "central line stepped" in self.plot_style:
                axes.plot(dataset.x_all_bin_edges, dataset.y_at_x_bin_edges, drawstyle="steps-pre", color=line_colour, linestyle=line_style, linewidth=line_width)
            else:
                _, _, barlinecols = axes.errorbar(dataset.x_points, dataset.y_points, xerr=np.transpose(dataset.x_error_pairs),
                                                  fmt="", markeredgewidth=0, linestyle="None", color=line_colour, linewidth=line_width)
                if line_style is not None:
                    barlinecols[0].set_linestyle(line_style)

        # Add the hatch colour if requested, this also adds an outline
        if self.plot_args["hatch"] is not None:
            self.plot_args["edgecolor"] = hatch_colour

        # Plot the band
        if plot_label is None:
            axes.fill_between(dataset.band_edges_x, dataset.band_edges_y_low, dataset.band_edges_y_high, **self.plot_args)
        else:
            axes.fill_between(dataset.band_edges_x, dataset.band_edges_y_low, dataset.band_edges_y_high, **self.plot_args)

            if "central line" in self.plot_style:
                proxy_artist = Ellipse((0, 0), 0, 0, axes=axes, label=plot_label, linestyle=line_style, facecolor=self.plot_args["facecolor"], edgecolor=line_colour)
                axes.add_patch(proxy_artist)
            else:
                proxy_artist = Rectangle((0, 0), 0, 0, axes=axes, label=plot_label, **self.plot_args)
                axes.add_patch(proxy_artist)
