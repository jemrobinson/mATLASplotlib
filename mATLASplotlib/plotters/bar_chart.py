"""This module provides the Bar class."""
import logging
from base_plotter import BasePlotter

logger = logging.getLogger("mATLASplotlib.plotters")


class BarChart(BasePlotter):
    """Plot bar chart."""

    def add_to_axes(self, axes, dataset, **kwargs):
        """Add to canvas."""
        logger.debug("Adding dataset to axes as bar")
        # Interpret arguments
        self.plot_args["color"] = kwargs.pop("colour", "black")                          # Default colour: black
        self.plot_args["label"] = kwargs.pop("label", None)                              # Default label: None
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 0.5)                       # Default linewidth: 0
        self.plot_args["edgecolor"] = kwargs.pop("edgecolour", self.plot_args["color"])  # Default edgecolour: match fill colour
        # Add any other user-provided arguments
        self.plot_args.update(kwargs)

        axes.bar(dataset.x_points, height=dataset.y_points, width=dataset.x_bin_widths, **self.plot_args)
