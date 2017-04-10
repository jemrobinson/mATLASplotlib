import logging

logger = logging.getLogger("mATLASplotlib.plotters")


class Bar(object):
    """Plot bar chart."""

    def __init__(self, plot_style):
        """Constructor."""
        self.plot_args = {}

    def add_to_axes(self, axes, dataset, **kwargs):
        """Add to canvas."""
        logger.debug("Adding dataset to axes as stack")
        # Interpret arguments
        self.plot_args["color"] = kwargs.pop("colour", "black")                          # Default colour: black
        self.plot_args["label"] = kwargs.pop("label", None)                              # Default label: None
        self.plot_args["linewidth"] = kwargs.pop("linewidth", 0.0)                       # Default linewidth: 0
        self.plot_args["edgecolor"] = kwargs.pop("edgecolour", self.plot_args["color"])  # Default edgecolour: match fill colour

        axes.bar(dataset.x_points, height=dataset.y_points, width=dataset.x_bin_widths, **self.plot_args)