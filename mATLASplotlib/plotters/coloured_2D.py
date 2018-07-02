"""This module provides the ``Coloured2D`` class."""
import logging
import matplotlib.pyplot as pyplot
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class Coloured2D(BasePlotter):
    """Plot as points in the x-y plane"""

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        """Add the chosen dataset to the chosen axes.

        :param axes: which axes to plot this dataset on
        :type axes: matplotlib.axes
        :param dataset: which axes to plot this dataset on
        :type dataset: matplotlib.axes

        :Keyword Arguments:
            * **colour_map** (*str*) -- which colour map to use
            * **with_key** (*bool*) -- draw the key (True by default)
        """
        # Construct plotting argument dictionary
        self.plot_args["cmap"] = getattr(pyplot.cm, kwargs.pop("colour_map", "Purples"))  # Default colour-map: Purples

        # Extract other known arguments from kwargs
        with_key = kwargs.pop("with_key", True)  # Default True

        # Add any other user-provided arguments
        self.plot_args.update(kwargs)

        x_values, y_values = dataset.construct_2D_bin_list(axes="xy")
        assert len(x_values) == len(y_values) == len(dataset.z_points)
        _, _, _, axes_image = axes.hist2d(x_values, y_values,
                                          bins=[dataset.x_bin_edges, dataset.y_bin_edges],
                                          weights=dataset.z_points, **self.plot_args)
        if with_key:
            colourbar = axes.get_figure().colorbar(axes_image, ax=axes, **self.plot_args)
            colourbar.solids.set_rasterized(True)
