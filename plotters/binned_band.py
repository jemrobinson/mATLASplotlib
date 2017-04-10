import logging
from matplotlib import pyplot
import numpy as np
from scipy import interpolate

logger = logging.getLogger("mATLASplotlib.plotters")

class BinnedBand(object):
    """Plot as binned band in the x-y plane"""
    def __init__(self, plot_style):
        self.plot_style = plot_style

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        # Construct plotting arguments
        plot_args = {}
        plot_args["facecolor"] = kwargs.pop("colour", "black")    # Default colour: black
        plot_args["edgecolor"] = kwargs.pop("background_colour", "white")    # Default colour: black
        plot_args["hatch"] = kwargs.pop("hatch", None)            # Default label: None
        plot_args["alpha"] = kwargs.pop("alpha", None)            # Default label: None
        plot_args["linewidth"] = kwargs.pop("linewidth", 0)       # Default linewidth: 2
        # plot_args["marker"] = kwargs.pop("marker", None)          # Default marker: dot
        plot_label = kwargs.pop("label", None)            # Default label: None

        if "filled" in self.plot_style:
            if plot_label == None:
                axes.fill_between(dataset.band_edges_x, dataset.band_edges_y_low, dataset.band_edges_y_high, **plot_args)
            else:
                axes.fill_between(dataset.band_edges_x, dataset.band_edges_y_low, dataset.band_edges_y_high, **plot_args)
                proxy_artist = pyplot.Rectangle((0, 0), 0, 0, axes=axes, label=plot_label, **plot_args)
                axes.add_patch(proxy_artist)
