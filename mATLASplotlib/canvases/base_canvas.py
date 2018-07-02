""" This module provides the ``BaseCanvas`` canvas."""
import logging
import math
import matplotlib
from .. import style
from ..converters import Dataset
from ..plotters import get_plotter
from ..decorations import draw_ATLAS_text, draw_text, Legend

logger = logging.getLogger("mATLASplotlib.canvases")


class BaseCanvas(object):
    """Base class for canvas properties."""

    location_map = {"upper right": ["right", "top"],
                    "upper left": ["left", "top"],
                    "centre left": ["left", "center"],
                    "centre right": ["right", "center"],
                    "lower right": ["right", "bottom"],
                    "lower left": ["left", "bottom"]}

    def __init__(self, shape="square", **kwargs):
        """Set up universal canvas properties.

        :param shape: use either the 'square' or 'landscape' ATLAS proportions
        :type shape: str

        :Keyword Arguments:
            * **log_type** (*str*) -- set 'x', 'y' or both ('xy') axes to log-scale
            * **x_ticks_extra** (*list*) -- list of additional minor ticks to label (only used when the x-axis is on a log scale)
            * **x_tick_labels** (*iterable*) -- list of tick labels for the x-axis
            * **x_tick_label_size** (*float*) -- fontsize for x-axis tick labels
            * **y_tick_labels** (*iterable*) -- list of tick labels for the y-axis
            * **y_tick_label_size** (*float*) -- fontsize for y-axis tick labels
        """
        # Set ATLAS style
        style.set_atlas()
        # Set up figure
        n_pixels = {"square": (600, 600), "landscape": (800, 600)}[shape]
        self.figure = matplotlib.pyplot.figure(figsize=(n_pixels[0] / 100.0, n_pixels[1] / 100.0), dpi=100, facecolor="white")
        self.main_subplot = None
        # Set properties from arguments
        self.log_type = kwargs.get("log_type", "")
        self.tick_labels = {"x": (kwargs.get("x_tick_labels", None), kwargs.get("x_tick_label_size", None)),
                            "y": (kwargs.get("y_tick_labels", None), kwargs.get("y_tick_label_size", None))}
        self.x_ticks_extra = kwargs.get("x_ticks_extra", [])
        # Set up value holders
        self.legend = Legend()
        self.axis_ranges = {}
        self.subplots = {}
        self.internal_header_fraction = None

    def __enter__(self):
        """Enter the runtime context related to this object.
        This object will be bound to the target of the `with` statement.
        """
        return self

    def __exit__(self, *args):
        """Exit the runtime context related to this object.
        The parameters describe the exception that caused the context to be exited.
        If the context was exited without an exception, all three arguments will be ``None``.
        """
        matplotlib.pyplot.close(self.figure)

    def plot_dataset(self, *args, **kwargs):
        """Plot a dataset.
        Non-keyword arguments will be interpreted as the dataset to be plotted.
        Keyword arguments will be interpreted as style arguments.

        :Positional Arguments:
            * **args**: (*ROOT.TObject*, *iterable*, *numpy array*) -- plottable information which is passed to `Dataset` to be interpreted

        :Keyword Arguments:
            * **remove_zeros**: (*bool*) -- prune any points in the dataset for which the y-value is 0
            * **axes**: (*str*) -- which axes to use (defaults to the main subplot)
            * **style**: (*str*) -- which of the plotters in `plotters` to use
            * **label**: (*str*) -- label to use in automatic legend generation
            * **sort_as**: (*str*) -- override
        """
        axes = kwargs.pop("axes", self.main_subplot)
        plot_style = kwargs.pop("style", None)
        remove_zeros = kwargs.pop("remove_zeros", False)
        dataset = Dataset(*args, remove_zeros=remove_zeros, **kwargs)
        plotter = get_plotter(plot_style)
        if "label" in kwargs:
            self.legend.add_dataset(label=kwargs["label"], is_stack=("stack" in plot_style), sort_as=kwargs.pop("sort_as", None))
        plotter.add_to_axes(dataset=dataset, axes=self.subplots[axes], **kwargs)

    def add_legend(self, x, y, anchor_to="lower left", fontsize=None, axes=None):
        """Add a legend to the canvas at (x, y).

        :param x: x position (as a fraction of the canvas width).
        :type x: float
        :param y: y position (as a fraction of the canvas height).
        :type y: float
        :param anchor_to: anchor point (one of the options in location_map).
        :type anchor_to: str
        :param fontsize: font size.
        :type fontsize: float
        :param axes: which of the different axes in this canvas to use.
        :type axes: str
        """
        if axes is None:
            axes = self.main_subplot
        self.legend.plot(x, y, self.subplots[axes], anchor_to, fontsize)

    def add_ATLAS_label(self, x, y, plot_type=None, anchor_to="lower left", fontsize=None, axes=None):
        """Add an ATLAS label to the canvas at (x, y).

        :param x: x position (as a fraction of the canvas width).
        :type x: float
        :param y: y position (as a fraction of the canvas height).
        :type y: float
        :param plot_type: Preliminary/Internal/Work-In-Progress/None
        :type plot_type: str
        :param anchor_to: anchor point (one of the options in location_map).
        :type anchor_to: str
        :param fontsize: font size.
        :type fontsize: float
        :param axes: which of the different axes in this canvas to use.
        :type axes: str
        """
        if axes is None:
            axes = self.main_subplot
        # ha, va = self.location_map[anchor_to]
        # draw_ATLAS_text(x, y, self.subplots[axes], ha=ha, va=va, plot_type=plot_type, fontsize=fontsize)
        draw_ATLAS_text(self.subplots[axes], (x, y), self.location_map[anchor_to], plot_type=plot_type, fontsize=fontsize)

    def add_luminosity_label(self, x, y, sqrts_TeV, luminosity, units="fb-1", anchor_to="lower left", fontsize=14, axes=None):
        """Add a luminosity label to the canvas at (x, y).

        :param x: x position (as a fraction of the canvas width).
        :type x: float
        :param y: y position (as a fraction of the canvas height).
        :type y: float
        :param sqrts_TeV: centre-of-mass energy in TeV.
        :type sqrts_TeV: float
        :param luminosity: luminosity.
        :type luminosity: float
        :param units: luminosity units.
        :type units: str
        :param anchor_to: anchor point (one of the options in location_map).
        :type anchor_to: str
        :param fontsize: font size.
        :type fontsize: float
        :param axes: which of the different axes in this canvas to use.
        :type axes: str
        """
        if axes is None:
            axes = self.main_subplot
        text_sqrts = r"$\sqrt{\mathsf{s}} = " +\
            str([sqrts_TeV, int(1000 * sqrts_TeV)][sqrts_TeV < 1.0]) +\
            r"\,\mathsf{" + ["TeV", "GeV"][sqrts_TeV < 1.0] + "}"
        text_lumi = "$" if luminosity is None else ", $" + str(luminosity) + " " + units.replace("-1", "$^{-1}$")
        draw_text(text_sqrts + text_lumi, self.subplots[axes], (x, y), self.location_map[anchor_to], fontsize=fontsize)

    def add_text(self, x, y, text, **kwargs):
        """Add text to the canvas at (x, y).

        :param x: x position (as a fraction of the canvas width).
        :type x: float
        :param y: y position (as a fraction of the canvas height).
        :type y: float
        :param text: text to add.
        :type text: str
        """
        axes = kwargs.pop("axes", self.main_subplot)
        anchor_to = kwargs.pop("anchor_to", "lower left")
        draw_text(text, self.subplots[axes], (x, y), self.location_map[anchor_to], **kwargs)

    def save(self, output_name, extension="pdf"):
        """Save the current state of the canvas to a file.

        :param output_name: name of output file.
        :type output_name: str
        :param extension: type of output to produce.
        :type extension: str or list
        """
        self.__finalise_plot_formatting()
        if isinstance(extension, str):
            extension = [extension]
        for output in extension:
            matplotlib.pyplot.savefig("{0}.{1}".format(output_name, output))
            logger.info("Saved figure to: {0}.{1}".format(output_name, output))

    def close(self):
        """Close the figure to free up memory.
        Not needed when this object is used as a context manager."""
        self.__exit__()

    def set_axis_label(self, axis_name, axis_label, fontsize=16):
        """Set the maximum value for the given axis.

        :param axis_name: which axis to apply this to.
        :type axis_name: str
        :param axis_label: desired label.
        :type axis_label: str
        :param fontsize: font size to use
        :type fontsize: float
        """
        raise NotImplementedError("set_label not defined by {0}".format(type(self)))

    def set_axis_max(self, axis_name, maximum):
        """Set the maximum value for the given axis.

        :param axis_name: which axis to apply this to.
        :type axis_name: str
        :param maximum: desired axis maximum.
        :type maximum: float
        """
        raise NotImplementedError("set_axis_max not defined by {0}".format(type(self)))

    def set_axis_min(self, axis_name, minimum):
        """Set the minimum value for the given axis.

        :param axis_name: which axis to apply this to.
        :type axis_name: str
        :param minimum: desired axis minimum.
        :type minimum: float
        """
        raise NotImplementedError("set_axis_min not defined by {0}".format(type(self)))

    def set_axis_range(self, axis_name, axis_range):
        """Set the range for the given axis.

        :param axis_name: which axis to apply this to.
        :type axis_name: str.
        :param axis_range: desired axis range.
        :type axis_range: iterable
        """
        raise NotImplementedError("set_axis_range not defined by {0}".format(type(self)))

    def set_axis_ticks(self, axis_name, ticks):
        """Set the position of the axis ticks.

        :param axis_name:  which axis to apply this to.
        :type axis_name: str
        :param ticks: desired tick positions.
        :type ticks: iterable
        """
        raise NotImplementedError("set_axis_ticks not defined by {0}".format(type(self)))

    def set_axis_log(self, axis_names):
        """Set the specified axis to be on a log-scale.

        :param axis_names: which axis (or axes) to apply this to.
        :type axis_names: str
        """
        self.log_type = axis_names

    def set_title(self, title):
        """Set the figure title.

        :param title: figure title to use
        :type title: str
        """
        raise NotImplementedError("set_title not defined by {0}".format(type(self)))

    @property
    def x_tick_labels(self):
        """Labels for x-ticks"""
        return self.tick_labels["x"][0]

    @property
    def x_tick_label_size(self):
        """Label size for x-ticks"""
        return self.tick_labels["x"][1]

    @property
    def y_tick_labels(self):
        """Labels for y-ticks"""
        return self.tick_labels["y"][0]

    @property
    def y_tick_label_size(self):
        """Label size for y-ticks"""
        return self.tick_labels["y"][1]

    def __finalise_plot_formatting(self):
        """Finalise plot by applying previously requested formatting."""
        for _, axes in self.subplots.items():
            # Apply axis limits
            self._apply_axis_limits()
            # Draw x ticks
            if self.x_tick_labels is not None:
                x_interval = (max(axes.get_xlim()) - min(axes.get_xlim())) / (len(self.x_tick_labels))
                axes.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(x_interval))
                tmp_kwargs = {"fontsize": self.x_tick_label_size} if self.x_tick_label_size is not None else {}
                axes.set_xticklabels([""] + self.x_tick_labels, **tmp_kwargs)  # the first and last ticks are off the scale so add a dummy label
            # Draw y ticks
            if self.y_tick_labels is not None:
                y_interval = (max(axes.get_ylim()) - min(axes.get_ylim())) / (len(self.y_tick_labels))
                axes.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(y_interval))
                tmp_kwargs = {"fontsize": self.y_tick_label_size} if self.y_tick_label_size is not None else {}
                axes.set_yticklabels([""] + self.y_tick_labels, **tmp_kwargs)  # the first and last ticks are off the scale so add a dummy label
            # Set x-axis locators
            if "x" in self.log_type:
                xlocator = axes.xaxis.get_major_locator()
                axes.set_xscale("log", subsx=[2, 3, 4, 5, 6, 7, 8, 9])
                axes.yaxis.set_major_locator(xlocator)
                axes.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
                axes.xaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(self.__force_extra_x_ticks))  # only show certain minor labels
            else:
                axes.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
            # Set y-axis locators
            if "y" in self.log_type:
                locator = axes.yaxis.get_major_locator()
                axes.set_yscale("log")
                axes.yaxis.set_major_locator(locator)
                fixed_minor_points = [10**x * val for x in range(-100, 100) for val in [2, 3, 4, 5, 6, 7, 8, 9]]
                axes.yaxis.set_minor_locator(matplotlib.ticker.FixedLocator(fixed_minor_points))
            else:
                axes.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())

        # Finish by adding internal header
        if self.internal_header_fraction is not None:
            y_lo, y_hi = self.subplots[self.main_subplot].get_ylim()
            y_top = (y_hi - self.internal_header_fraction * y_lo) / (1.0 - self.internal_header_fraction)
            if "y" in self.log_type:
                y_top = math.exp((math.log(y_hi) - self.internal_header_fraction * math.log(y_lo)) / (1.0 - self.internal_header_fraction))
            self.subplots[self.main_subplot].set_ylim(y_lo, y_top)

        # Call child formatter if available
        self._apply_final_formatting()

    def _apply_axis_limits(self):
        """Apply the previously defined axis limits."""
        raise NotImplementedError("_apply_axis_limits not defined by {0}".format(type(self)))

    def _apply_final_formatting(self):
        """Apply any necessary final formatting."""
        pass

    def __force_extra_x_ticks(self, x, pos):
        """Implement user-defined tick positions.

        :param x: tick value.
        :type x: float
        :param pos: position.
        :type pos: float
        :return: formatted tick position string
        :rtype: str
        """
        del pos  # this function signature is required by FuncFormatter
        if any(int(x) == elem for elem in self.x_ticks_extra):
            return "{0:.0f}".format(x)
        return ""

    def get_axis_label(self, axis_name):
        """Get the label for the chosen axis

        :param axis_name: which axis to use.
        :type axis_name: str
        :return: axis label
        :rtype: str
        """
        raise NotImplementedError("get_label not defined by {0}".format(type(self)))

    def get_axis_range(self, axis_name):
        """Get the range for the chosen axis

        :param axis_name: which axis to use.
        :type axis_name: str
        :return: axis range
        :rtype: tuple
        """
        if axis_name in self.axis_ranges.keys():
            return self.axis_ranges[axis_name]
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))
