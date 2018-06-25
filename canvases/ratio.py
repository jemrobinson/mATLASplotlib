from base_canvas import BaseCanvas
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, MaxNLocator
from numpy import arange


class Ratio(BaseCanvas):
    """Ratio canvas with standard ATLAS setup"""

    def __init__(self, n_pixels=(600, 600), line_ypos=1.0, **kwargs):
        super(Ratio, self).__init__(n_pixels, **kwargs)
        self.subplots["top"] = self.figure.add_axes([0.15, 0.35, 0.8, 0.6])
        self.subplots["bottom"] = self.figure.add_axes([0.15, 0.1, 0.8, 0.25])
        self.main_subplot = "top"
        self.axis_ranges["y_ratio"] = [0.5, 1.5]
        self.line_ypos = line_ypos

    def plot_dataset(self, *args, **kwargs):
        axes = kwargs.get("axes", self.main_subplot)
        super(Ratio, self).plot_dataset(*args, **kwargs)
        if "x" not in self.axis_ranges:
            self.set_axis_range("x", self.subplots[axes].get_xlim())
        if axes == "top":
            if "y" not in self.axis_ranges:
                self.set_axis_range("y", self.subplots[axes].get_ylim())
        elif axes == "bottom":
            if "y_ratio" not in self.axis_ranges:
                self.set_axis_range("y_ratio", self.subplots[axes].get_ylim())

    def apply_axis_limits(self):
        if "x" in self.axis_ranges:
            self.subplots["top"].set_xlim(self.axis_ranges["x"])
            self.subplots["bottom"].set_xlim(self.axis_ranges["x"])
        if "y" in self.axis_ranges:
            self.subplots["top"].set_ylim(self.axis_ranges["y"])
        if "y_ratio" in self.axis_ranges:
            self.subplots["bottom"].set_ylim(self.axis_ranges["y_ratio"])

    def apply_final_formatting(self):
        # Draw line at y = line_ypos
        self.subplots["bottom"].add_line(Line2D(self.subplots["bottom"].get_xlim(), [self.line_ypos, self.line_ypos], transform=self.subplots["bottom"].transData, linewidth=1, linestyle="--", color="black"))

        # Set ratio plot to linear scale
        if self.log_type.find("y") != -1:
            self.subplots["bottom"].set_yscale("linear")

        # Remove tick-labels from top-plot
        self.subplots["top"].set_xticklabels([], minor=True)
        self.subplots["top"].set_xticklabels([], major=True)

    # Provide defaults for inherited methods
    def draw_ATLAS_text(self, x, y, axes="top", **kwargs):
        super(Ratio, self).draw_ATLAS_text(x, y, axes=axes, **kwargs)

    def draw_legend(self, x, y, axes="top", **kwargs):
        super(Ratio, self).draw_legend(x, y, axes=axes, **kwargs)

    def draw_luminosity_text(self, x, y, luminosity_value, axes="top", **kwargs):
        super(Ratio, self).draw_luminosity_text(x, y, luminosity_value, axes=axes, **kwargs)

    def draw_text(self, x, y, extra_value, axes="top", **kwargs):
        super(Ratio, self).draw_text(x, y, extra_value, axes=axes, **kwargs)

    def get_ratio_ticks(self, axis_range, n_approximate=4):
        # Choose ratio ticks to be sensibly spaced and always include 1.0
        interval_estimate = abs(axis_range[1] - axis_range[0]) / float(n_approximate)
        tick_sizes = [0.001, 0.002, 0.005, 0.01, 0.02, 0.04, 0.05, 0.1, 0.2, 0.4, 0.5, 1.0, 2.0]
        tick_size = min(tick_sizes, key=lambda x: abs(x - interval_estimate))
        return arange(1.0 - 10 * tick_size, 1.0 + 10 * tick_size, tick_size)

    # Axis labels
    def get_axis_label(self, axis_name):
        if axis_name == "x":
            return self.subplots["bottom"].get_xlabel()
        elif axis_name == "y":
            return self.subplots["top"].get_ylabel()
        elif axis_name == "y_ratio":
            self.subplots["bottom"].get_ylabel()
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_label(self, axis_name, axis_label, **kwargs):
        fontsize = kwargs.pop("fontsize", 16)
        if axis_name == "x":
            self.subplots["bottom"].set_xlabel(axis_label, fontsize=fontsize, position=(1.0, 0.0), va="top", ha="right", *kwargs)
        elif axis_name == "y":
            self.subplots["top"].set_ylabel(axis_label, fontsize=fontsize)
            self.subplots["top"].yaxis.get_label().set_ha("right")
            self.subplots["top"].yaxis.set_label_coords(-0.13, 1.0)
        elif axis_name == "y_ratio":
            self.subplots["bottom"].set_ylabel(axis_label, fontsize=fontsize)
            self.subplots["bottom"].yaxis.get_label().set_ha("center")
            self.subplots["bottom"].yaxis.set_label_coords(-0.13, 0.5)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_labels(self, x_axis_label, y_axis_label, ratio_y_axis_label):
        self.set_axis_label("x", x_axis_label)
        self.set_axis_label("y", y_axis_label)
        self.set_axis_label("y_ratio", ratio_y_axis_label)

    # Axis ranges
    def set_axis_max(self, axis_name, maximum):
        if axis_name == "x":
            self.subplots["top"].set_xlim(top=maximum)
            self.subplots["bottom"].set_xlim(top=maximum)
        elif axis_name == "y":
            self.subplots["top"].set_ylim(top=maximum)
        elif axis_name == "y_ratio":
            self.subplots["bottom"].set_ylim(top=maximum)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_min(self, axis_name, minimum):
        if axis_name == "x":
            self.subplots["top"].set_xlim(bottom=minimum)
            self.subplots["bottom"].set_xlim(bottom=minimum)
        elif axis_name == "y":
            self.subplots["top"].set_ylim(bottom=minimum)
        elif axis_name == "y_ratio":
            self.subplots["bottom"].set_ylim(bottom=minimum)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))
        if axis_name in self.axis_ranges:
            self.axis_ranges[axis_name] = (minimum, self.axis_ranges[axis_name][1])


    def set_axis_range(self, axis_name, axis_range):
        if axis_name == "x":
            self.axis_ranges["x"] = axis_range
        elif axis_name == "y":
            self.axis_ranges["y"] = axis_range
        elif axis_name == "y_ratio":
            self.axis_ranges["y_ratio"] = axis_range
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_ticks(self, axis_name, ticks, force=False):
        """Document here."""
        if axis_name == "x":
            self.subplots["top"].xaxis.set_major_locator(FixedLocator(ticks))
        elif axis_name == "y":
            self.subplots["top"].yaxis.set_major_locator(FixedLocator(ticks))
        elif axis_name == "y_ratio":
            self.subplots["bottom"].yaxis.set_major_locator(FixedLocator(ticks))
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_ranges(self, x_axis_range, y_axis_range, ratio_y_axis_range):
        self.set_axis_range("x", x_axis_range)
        self.set_axis_range("y", y_axis_range)
        self.set_axis_range("y_ratio", ratio_y_axis_range)

    # Plot title
    def set_title(self, title):
        self.subplots["top"].set_title(title)
