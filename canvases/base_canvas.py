import logging
import math
import matplotlib
from .. import style
from ..converters import Dataset
from ..plotters import get_plotter
from ..decorations import ATLAS_text, Legend, Text

logger = logging.getLogger("mATLASplotlib.canvases")
# matplotlib.use("PDF")


class BaseCanvas(object):
    """Base class for canvas properties."""

    location_map = {"upper right": ["right", "top"], "upper left": ["left", "top"], "lower right": ["right", "bottom"], "lower left": ["left", "bottom"]}

    def __init__(self, n_pixels, **kwargs):
        """Constructor."""
        # Set ATLAS style
        style.set_atlas()
        # Set up figure
        self.figure = matplotlib.pyplot.figure(figsize=(n_pixels[0] / 100.0, n_pixels[1] / 100.0), dpi=100, facecolor="white")
        self.main_subplot = None
        # Set properties from arguments
        self.log_type = kwargs.get("log_type", "")
        self.x_ticks = kwargs.get("x_ticks", None)
        self.x_tick_size = kwargs.get("x_tick_size", None)
        self.minor_x_ticks = kwargs.get("minor_x_ticks", [])
        # Set up value holders
        self.legend = Legend()
        self.axis_ranges = {}
        self.subplots = {}
        self.internal_header_fraction = None

    def plot_dataset(self, dataset, style, axes=None, **kwargs):
        """Document here."""
        if not isinstance(dataset, Dataset):
            if hasattr(dataset, '__iter__'): dataset = Dataset(*dataset)
            else: dataset = Dataset(dataset)
        if axes is None: axes = self.main_subplot
        if "label" in kwargs:
            self.legend.add_dataset(label=kwargs["label"], visible_label=kwargs.get("visible_label", None), is_stack=("stack" in style))
        get_plotter(style).add_to_axes(dataset=dataset, axes=self.subplots[axes], **kwargs)

    def __finalise_plot_formatting(self):
        """Set useful axis properties."""
        for axes in self.figure.axes:
            # Draw x ticks
            if self.x_ticks is not None:
                x_interval = (axes.get_xlim()[1] - axes.get_xlim()[0]) / len(self.x_ticks)
                axes.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(x_interval))
                if self.x_tick_size is None:
		    axes.set_xticklabels([""] + self.x_ticks)  # for some reason the first label is getting lost
                else:
                    axes.set_xticklabels([""] + self.x_ticks, fontsize=self.x_tick_size)  # for some reason the first label is getting lost
            # Draw minor ticks
            axes.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
            axes.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
            # Set x-axis log
            if "x" in self.log_type:
                axes.set_xscale("log", subsx=[2, 3, 4, 5, 6, 7, 8, 9])
                axes.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
                axes.xaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(self.minor_tick_format_function))  # only show certain minor labels
            # Set y-axis log
            if "y" in self.log_type:
                axes.set_yscale("log", subsy=[2, 3, 4, 5, 6, 7, 8, 9])
        # Call child formatter if available
        if hasattr(self, "_finalise"):
            self._finalise()
        # Finish by adding internal header
        if self.internal_header_fraction is not None:
            y_lo, y_hi = self.subplots[self.main_subplot].get_ylim()
            y_top = (y_hi - self.internal_header_fraction * y_lo) / (1.0 - self.internal_header_fraction)
            if "y" in self.log_type: y_top = math.exp((math.log(y_hi) - self.internal_header_fraction * math.log(y_lo)) / (1.0 - self.internal_header_fraction))
            self.subplots[self.main_subplot].set_ylim(y_lo, y_top)

    def add_legend(self, x, y, axes=None, anchor_to="lower left", fontsize=None):
        """Document here."""
        if axes is None: axes = self.main_subplot
        self.legend.draw(x, y, self.subplots[axes], anchor_to, fontsize)

    def add_ATLAS_label(self, x, y, plot_type=None, axes=None, anchor_to="lower left", fontsize=None):
        """Document here."""
        if axes is None: axes = self.main_subplot
        ATLAS_text(plot_type).draw(x, y, self.subplots[axes], ha=self.location_map[anchor_to][0], va=self.location_map[anchor_to][1], fontsize=fontsize)

    def add_luminosity_label(self, x, y, sqrts_TeV, luminosity, units="fb-1", axes=None, anchor_to="lower left", fontsize=None):
        """Document here."""
        if axes is None: axes = self.main_subplot
        fontsize = [fontsize, 14][fontsize is None]
        text_sqrts = r"$\mathrm{\mathsf{\sqrt{s}}} = " + str([sqrts_TeV, int(1000 * sqrts_TeV)][sqrts_TeV < 1.0]) + "\,\mathrm{\mathsf{" + ["TeV", "GeV"][sqrts_TeV < 1.0] + "}}"
        text_lumi = ["\quad \mathcal{L} = $" + str(luminosity) + " " + units.replace("-1", "$^{-1}$"), "$"][luminosity is None]
        text = text_sqrts + text_lumi
        Text(text).draw(x, y, self.subplots[axes], ha=self.location_map[anchor_to][0], va=self.location_map[anchor_to][1], fontsize=fontsize)

    def add_text(self, x, y, text, axes=None, anchor_to="lower left", fontsize=None):
        """Document here."""
        if axes is None: axes = self.main_subplot
        Text(text).draw(x, y, self.subplots[axes], ha=self.location_map[anchor_to][0], va=self.location_map[anchor_to][1], fontsize=fontsize)

    def get_axis_label(self, axis_name):
        """Document here."""
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
        self.__finalise_plot_formatting()
        matplotlib.pyplot.savefig("{0}.{1}".format(output_name, extension))
        logger.info("Saved figure to: {0}.{1}".format(output_name, extension))
        matplotlib.pyplot.close(self.figure)

    def set_axis_label(self, axis_name, axis_label):
        """Document here."""
        raise NotImplementedError("set_label not defined by {0}".format(type(self)))

    def set_axis_range(self, axis_name, axis_range):
        """Document here."""
        raise NotImplementedError("set_axis_range not defined by {0}".format(type(self)))

    def set_axis_log(self, log_type):
        """Document here."""
        self.log_type = log_type

    def set_title(self, title):
        """Document here."""
        raise NotImplementedError("set_title not defined by {0}".format(type(self)))
