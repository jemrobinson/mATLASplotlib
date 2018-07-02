"""This module provides the ``BarChart`` class."""
import logging
from matplotlib.patches import Rectangle
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class BarChart(BasePlotter):
    """Plot bar chart."""

    def add_to_axes(self, axes, dataset, **kwargs):
        """Add the chosen dataset to the chosen axes.

        :param axes: which axes to plot this dataset on
        :type axes: matplotlib.axes
        :param dataset: which axes to plot this dataset on
        :type dataset: matplotlib.axes

        :Keyword Arguments:
            * **colour** (*str*) -- which face colour to use
            * **edgecolour** (*float*) -- which colour to use for the outline
            * **edgewidth** (*float*) -- how large an outline width to use
            * **label** (*str*) -- label to use when this appears in a legend
        """
        logger.debug("Adding dataset to axes as bar")
        # Construct plotting argument dictionary
        self.plot_args["color"] = kwargs.pop("colour", "black")  # Default colour: black

        # Extract other known arguments from kwargs
        edgecolour = kwargs.pop("edgecolour", None)              # Default edgecolour: None
        linewidth = kwargs.pop("edgewidth", 4)                   # Default linewidth: 4
        label = kwargs.pop("label", None)                        # Default label: None

        # Add any other user-provided arguments
        self.plot_args.update(kwargs)

        # First draw the edges if requested
        if edgecolour is not None:
            axes.bar(dataset.x_points, height=dataset.y_points, width=dataset.x_bin_widths, color=None, edgecolor=edgecolour, linewidth=linewidth)

        # Draw main bar - expand the widths slightly to fill in zero-width gaps
        axes.bar(dataset.x_points, height=dataset.y_points, width=[1.004 * x for x in dataset.x_bin_widths], edgecolor=None, **self.plot_args)

        # Add a proxy artist with correct edge and facecolours
        if edgecolour is None:
            axes.add_patch(Rectangle((0, 0), 0, 0, axes=axes, label=label, linewidth=0.5 * linewidth, facecolor=self.plot_args["color"]))
        else:
            axes.add_patch(Rectangle((0, 0), 0, 0, axes=axes, label=label, linewidth=0.5 * linewidth, facecolor=self.plot_args["color"], edgecolor=edgecolour))
