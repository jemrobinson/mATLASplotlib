import matplotlib; matplotlib.use("PDF")
import matplotlib.pyplot as pyplot
import logging
from .. import style
from ..plotting import get_plotter
from ..decorations import ATLAS_text, Legend, Text

logger = logging.getLogger("mATLASplotlib.canvases")

class BaseCanvas(object):
    # Class-level variables
    location_map = {"upper right":["right", "top"], "upper left":["left", "top"], "lower right":["right", "bottom"], "lower left":["left", "bottom"]}

    def __init__(self, n_pixels, **kwargs):
        """Base class for canvas properties"""
        # Set ATLAS style
        style.set_atlas()

        # Set up figure
        self.figure = pyplot.figure(figsize=(n_pixels[0] / 100.0, n_pixels[1] / 100.0), dpi=100, facecolor="white")
        self.main_subplot = None

        # Set properties from arguments
        self.log_type = kwargs.get("log_type", "")
        self.x_ticks = kwargs.get("x_ticks", None)
        self.minor_x_ticks = kwargs.get("minor_x_ticks", [])

        # Set up value holders
        self.legend = Legend()
        self.axis_ranges = {}
        self.subplots = {}
        self.internal_header_fraction = None


    def plot_dataset(self, dataset, style, axes=None, **kwargs):
        if axes is None: axes = self.main_subplot
        if "label" in kwargs:
            self.legend.add_dataset(label=kwargs["label"], visible_label=kwargs.get("visible_label", None), is_stack=("stack" in style))
        get_plotter(style).add_to_axes(dataset=dataset, axes=self.subplots[axes], **kwargs)


    def __finalise_plot_formatting(self):
        # Set useful axis properties
        for axes in self.figure.axes:
            # Draw x ticks
            if self.x_ticks is not None:
                x_interval = (self.axis_ranges["x"][1] - self.axis_ranges["x"][0]) / len(self.x_ticks)
                axes.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(x_interval))
                axes.set_xticklabels([""] + self.x_ticks)  # for some reason the first label is getting lost

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
            self.subplots[self.main_subplot].set_ylim(y_lo, y_hi / (1.0 - self.internal_header_fraction))


    def add_legend(self, x, y, axes=None, anchor_to="lower left", fontsize=None):
        if axes is None: axes = self.main_subplot
        self.legend.draw(x, y, self.subplots[axes], anchor_to, fontsize)

    def add_ATLAS_label(self, x, y, plot_type=None, axes=None,anchor_to="lower left", fontsize=None):
        if axes is None: axes = self.main_subplot
        ATLAS_text(plot_type).draw(x, y, self.subplots[axes], ha=self.location_map[anchor_to][0], va=self.location_map[anchor_to][1], fontsize=fontsize)

    def add_luminosity_label(self, x, y, luminosity_pb, sqrts_TeV, axes=None, anchor_to="lower left", fontsize=None):
        if axes is None: axes = self.main_subplot
        fontsize = [fontsize, 14][fontsize==None]
        # text = r"$\mathrm{\mathsf{\sqrt{s}}} = " + str(sqrts_TeV) + "\,\mathrm{\mathsf{TeV}} \, \int \mathcal{L} \mathrm{dt} = $" + str(luminosity_pb) + " pb$^{-1}$"
        text = r"$\mathrm{\mathsf{\sqrt{s}}} = " + str(sqrts_TeV) + "\,\mathrm{\mathsf{TeV}} \quad \mathcal{L} = $" + str(luminosity_pb) + " pb$^{-1}$"
        Text(text).draw(x, y, self.subplots[axes], ha=self.location_map[anchor_to][0], va=self.location_map[anchor_to][1], fontsize=fontsize)

    def add_text(self, x, y, text, axes=None, anchor_to="lower left", fontsize=None):
        if axes is None: axes = self.main_subplot
        Text(text).draw(x, y, self.subplots[axes], ha=self.location_map[anchor_to][0], va=self.location_map[anchor_to][1], fontsize=fontsize)

    def get_axis_label(self, axis_name):
        raise NotImplementedError("get_label not defined by {0}".format(type(self)))


    def get_axis_range(self, axis_name):
        if axis_name in self.axis_ranges.keys():
            return self.axis_ranges[axis_name]
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))


    def minor_tick_format_function(self, x, pos):
        if any(int(x) == elem for elem in self.minor_x_ticks):
            return "{0:.0f}".format(x)
        return ""


    def save_to_file(self, output_name):
        self.__finalise_plot_formatting()
        pyplot.savefig("{0}.pdf".format(output_name))
        logger.info("Saved figure to: {0}.pdf".format(output_name))
        pyplot.close(self.figure)


    def set_axis_label(self, axis_name, axis_label):
        raise NotImplementedError("set_label not defined by {0}".format(type(self)))


    def set_axis_range(self, axis_name, axis_range):
        raise NotImplementedError("set_axis_range not defined by {0}".format(type(self)))

    def set_axis_log(self, log_type):
        self.log_type = log_type

    def set_title(self, title):
        raise NotImplementedError("set_title not defined by {0}".format(type(self)))


    # def translate_coordinates(self, coordinates, axes):
    #     if coordinates == "axes":
    #         return self.subplots[axes].transAxes
    #     return self.figure.transFigure