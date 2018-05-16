import logging
import math
import matplotlib
from .. import style
from ..converters import Dataset
from ..plotters import get_plotter
from ..decorations import ATLAS_text, Legend, Text

logger = logging.getLogger("mATLASplotlib.canvases")


class BaseCanvas(object):
    """Base class for canvas properties."""

    location_map = {"upper right": ["right", "top"], "upper left": ["left", "top"], "centre left": ["left", "center"], "centre right": ["right", "center"], "lower right": ["right", "bottom"], "lower left": ["left", "bottom"]}

    def __init__(self, n_pixels, **kwargs):
        """Constructor."""
        # Set ATLAS style
        style.set_atlas()
        # Set up figure
        self.figure = matplotlib.pyplot.figure(figsize=(n_pixels[0] / 100.0, n_pixels[1] / 100.0), dpi=100, facecolor="white")
        self.main_subplot = None
        # Set properties from arguments
        self.log_type = kwargs.get("log_type", "")
        self.x_tick_labels = kwargs.get("x_tick_labels", None)
        self.x_tick_label_size = kwargs.get("x_tick_label_size", None)
        self.minor_x_ticks = kwargs.get("minor_x_ticks", [])
        # Set up value holders
        self.legend = Legend()
        self.axis_ranges = {}
        self.subplots = {}
        self.internal_header_fraction = None

    def plot_dataset(self, *args, **kwargs):
        """Plot a dataset, converting arguments as appropriate."""
        remove_zeros = kwargs.pop("remove_zeros", False)
        if not isinstance(args, Dataset):
            if hasattr(args, "__iter__"):
                dataset = Dataset(*args, remove_zeros=remove_zeros, **kwargs)
            else:
                dataset = Dataset(args, remove_zeros=remove_zeros, **kwargs)
        axes = kwargs.pop("axes", self.main_subplot)
        plot_style = kwargs.pop("style", None)
        plotter = get_plotter(plot_style)
        if "label" in kwargs:
            self.legend.add_dataset(label=kwargs["label"], visible_label=kwargs.get("visible_label", None), is_stack=("stack" in plot_style), sort_as=kwargs.pop("sort_as", None))
        plotter.add_to_axes(dataset=dataset, axes=self.subplots[axes], **kwargs)

    def finalise_plot_formatting(self):
        """Set useful axis properties."""
        for _, axes in self.subplots.items():
            # Apply axis limits
            self.apply_axis_limits()
            # Draw x ticks
            if self.x_tick_labels is not None:
                x_tick_locations = axes.xaxis.get_major_locator()()
                x_interval = (max(x_tick_locations) - min(x_tick_locations)) / (len(x_tick_locations) - 1)
                axes.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(x_interval))
                tmp_kwargs = {"fontsize": self.x_tick_label_size} if self.x_tick_label_size is not None else {}
                axes.set_xticklabels([""] + self.x_tick_labels, **tmp_kwargs) # the first and last ticks are off the scale so add a dummy label
            # Set x-axis locators
            if "x" in self.log_type:
                xlocator = axes.xaxis.get_major_locator()
                axes.set_xscale("log", subsx=[2, 3, 4, 5, 6, 7, 8, 9])
                axes.yaxis.set_major_locator(xlocator)
                axes.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
                axes.xaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(self.minor_tick_format_function))  # only show certain minor labels
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
            if "y" in self.log_type: y_top = math.exp((math.log(y_hi) - self.internal_header_fraction * math.log(y_lo)) / (1.0 - self.internal_header_fraction))
            self.subplots[self.main_subplot].set_ylim(y_lo, y_top)

        # Call child formatter if available
        self.apply_final_formatting()


    def add_legend(self, x, y, axes=None, anchor_to="lower left", fontsize=None):
        """Document here."""
        if axes is None:
            axes = self.main_subplot
        self.legend.draw(x, y, self.subplots[axes], anchor_to, fontsize)

    def add_ATLAS_label(self, x, y, plot_type=None, axes=None, anchor_to="lower left", fontsize=None):
        """Document here."""
        if axes is None:
            axes = self.main_subplot
        ATLAS_text(plot_type).draw(x, y, self.subplots[axes], ha=self.location_map[anchor_to][0], va=self.location_map[anchor_to][1], fontsize=fontsize)

    def add_luminosity_label(self, x, y, sqrts_TeV, luminosity, units="fb-1", axes=None, anchor_to="lower left", fontsize=14):
        """Document here."""
        if axes is None:
            axes = self.main_subplot
        text_sqrts = r"$\mathrm{\mathsf{\sqrt{s}}} = " + str([sqrts_TeV, int(1000 * sqrts_TeV)][sqrts_TeV < 1.0]) + r"\,\mathrm{\mathsf{" + ["TeV", "GeV"][sqrts_TeV < 1.0] + "}}"
        text_lumi = ", $" + str(luminosity) + " " + units.replace("-1", "$^{-1}$") if luminosity is not None else "$"
        text = text_sqrts + text_lumi
        Text(text).draw(x, y, self.subplots[axes], ha=self.location_map[anchor_to][0], va=self.location_map[anchor_to][1], fontsize=fontsize)

    def add_text(self, x, y, text, **kwargs):
        """Document here."""
        axes = kwargs.pop("axes", self.main_subplot)
        anchor_to = kwargs.pop("anchor_to", "lower left")
        Text(text).draw(x, y, self.subplots[axes], ha=self.location_map[anchor_to][0], va=self.location_map[anchor_to][1], **kwargs)

    def apply_axis_limits(self):
        """Should be overridden by child classes"""
        raise NotImplementedError("apply_axis_limits not defined by {0}".format(type(self)))

    def apply_final_formatting(self):
        """Should be overridden by child classes"""
        raise NotImplementedError("apply_final_formatting not defined by {0}".format(type(self)))

    def get_axis_label(self, axis_name):
        """Should be overridden by child classes"""
        raise NotImplementedError("get_label not defined by {0}".format(type(self)))

    def get_axis_range(self, axis_name):
        """Document here."""
        if axis_name in self.axis_ranges.keys():
            return self.axis_ranges[axis_name]
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def minor_tick_format_function(self, x, pos):
        """Document here."""
        if any(int(x) == elem for elem in self.minor_x_ticks):
            return "{0:.0f}".format(x)
        return ""

    def save_to_file(self, output_name, extension="pdf"):
        """Document here."""
        self.finalise_plot_formatting()
        matplotlib.pyplot.savefig("{0}.{1}".format(output_name, extension))
        logger.info("Saved figure to: {0}.{1}".format(output_name, extension))
        matplotlib.pyplot.close(self.figure)

    def set_axis_label(self, axis_name, axis_label):
        """Document here."""
        raise NotImplementedError("set_label not defined by {0}".format(type(self)))

    def set_axis_max(self, axis_name, maximum):
        """Document here."""
        raise NotImplementedError("set_axis_max not defined by {0}".format(type(self)))

    def set_axis_min(self, axis_name, minimum):
        """Document here."""
        raise NotImplementedError("set_axis_min not defined by {0}".format(type(self)))

    def set_axis_range(self, axis_name, axis_range):
        """Document here."""
        raise NotImplementedError("set_axis_range not defined by {0}".format(type(self)))

    def set_axis_ticks(self, axis_name, ticks, force=False):
        """Document here."""
        raise NotImplementedError("set_axis_ticks not defined by {0}".format(type(self)))

    def set_axis_log(self, log_type):
        """Document here."""
        self.log_type = log_type

    def set_title(self, title):
        """Document here."""
        raise NotImplementedError("set_title not defined by {0}".format(type(self)))
