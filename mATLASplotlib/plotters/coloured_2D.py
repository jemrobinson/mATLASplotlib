"""This module provides the Coloured2D class."""
import logging
import matplotlib.pyplot as pyplot
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class Coloured2D(BasePlotter):
    """Plot as points in the x-y plane"""

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        # Construct plotting arguments
        self.plot_args["cmap"] = getattr(pyplot.cm, kwargs.pop("colour_map", "Purples"))  # Default colour-map: Purples
        # Add any other user-provided arguments
        self.plot_args.update(kwargs)
        x_values, y_values = dataset.unroll_bins(axes="xy")
        assert len(x_values) == len(y_values) == len(dataset.z_points)
        _, _, _, axes_image = axes.hist2d(x_values, y_values,
                                          bins=[dataset.x_bin_edges, dataset.y_bin_edges],
                                          weights=dataset.z_points, **self.plot_args)
        colourbar = axes.get_figure().colorbar(axes_image, ax=axes, **self.plot_args)
        colourbar.solids.set_rasterized(True)
