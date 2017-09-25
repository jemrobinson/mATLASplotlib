from base_plotter import BasePlotter
from matplotlib import pyplot
from scipy import interpolate
import logging
import numpy as np

logger = logging.getLogger("mATLASplotlib.plotters")

class BinnedBand(BasePlotter):
    """Plot as binned band in the x-y plane"""
    def __init__(self, plot_style):
        """Constructor."""
        super(BinnedBand, self).__init__(plot_style)

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        # Construct plotting arguments
        self.plot_args["facecolor"] = kwargs.pop("colour", "black")            # Default colour: black
        self.plot_args["edgecolor"] = kwargs.pop("background_colour", "white") # Default colour: white
        self.plot_args["hatch"] = kwargs.pop("hatch", None)                    # Default label: None
        self.plot_args["alpha"] = kwargs.pop("alpha", None)                    # Default label: None
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 0)               # Default linewidth: 2
        # Add any other user-provided arguments
        self.plot_args.update(kwargs)
        plot_label = kwargs.pop("label", None)            # Default label: None

        if plot_label == None:
            axes.fill_between(dataset.band_edges_x, dataset.band_edges_y_low, dataset.band_edges_y_high, **self.plot_args)
        else:
            axes.fill_between(dataset.band_edges_x, dataset.band_edges_y_low, dataset.band_edges_y_high, **self.plot_args)
            proxy_artist = pyplot.Rectangle((0, 0), 0, 0, axes=axes, label=plot_label, **self.plot_args)
            axes.add_patch(proxy_artist)
