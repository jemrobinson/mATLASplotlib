import logging
from matplotlib import __version__ as mpl_version
import numpy as np

logger = logging.getLogger("mATLASplotlib.plotters")

class Stack(object):
    """Plot as points in the x-y plane"""
    def __init__(self, plot_style):
        self.plot_args = {}

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        logger.debug("Adding dataset to axes as stack")
        # Interpret arguments
        self.plot_args["color"] = kwargs.pop("colour", "black")                         # Default colour: black
        self.plot_args["label"] = kwargs.pop("label", None)                             # Default label: None
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 0.0)                      # Default linewidth: 0
        self.plot_args["edgecolor"] = kwargs.pop("edgecolour", self.plot_args["color"]) # Default edgecolour: match fill colour
        if not hasattr(axes, 'stack_bottom'):
            axes.stack_bottom = [0] * len(dataset.y_points)
        axes.bar(dataset.x_bin_low_edges, height=dataset.y_points, width=dataset.x_bin_widths, bottom=axes.stack_bottom, **self.plot_args)
        axes.stack_bottom = [increment + previous for increment, previous in zip(dataset.y_points, axes.stack_bottom)]
