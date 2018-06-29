""" This module provides the Ratio canvas."""
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator
from numpy import arange
from base_canvas import BaseCanvas


class Ratio(BaseCanvas):
    """Ratio canvas with standard ATLAS setup"""

    def __init__(self, shape="square", line_ypos=1.0, **kwargs):
        """Set up Ratio canvas properties.

        :param shape: use either the 'square' or 'rectangular' ATLAS proportions
        :type shape: str
        :param line_ypos: where to draw the reference line in the ratio plot
        :type line_ypos: float

        :Keyword Arguments: as for `BaseCanvas`
        """
        super(Ratio, self).__init__(shape=shape, **kwargs)
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

    def _apply_axis_limits(self):
        if "x" in self.axis_ranges:
            self.subplots["top"].set_xlim(self.axis_ranges["x"])
            self.subplots["bottom"].set_xlim(self.axis_ranges["x"])
        if "y" in self.axis_ranges:
            self.subplots["top"].set_ylim(self.axis_ranges["y"])
        if "y_ratio" in self.axis_ranges:
            self.subplots["bottom"].set_ylim(self.axis_ranges["y_ratio"])

    def _apply_final_formatting(self):
        """Apply final formatting. Draw line at y = line_ypos"""
        self.subplots["bottom"].add_line(Line2D(self.subplots["bottom"].get_xlim(),
                                                [self.line_ypos, self.line_ypos],
                                                transform=self.subplots["bottom"].transData,
                                                linewidth=1, linestyle="--", color="black"))

        # Set ratio plot to linear scale
        if self.log_type.find("y") != -1:
            self.subplots["bottom"].set_yscale("linear")

        # Remove tick-labels from top-plot
        self.subplots["top"].set_xticklabels([], minor=True)
        self.subplots["top"].set_xticklabels([], major=True)

    def get_ratio_ticks(self, axis_range, n_approximate=4):
        """Choose ratio ticks to be sensibly spaced and always include 1.0"""
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
            return self.subplots["bottom"].get_ylabel()
        raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_label(self, axis_name, axis_label, fontsize=16):
        if axis_name == "x":
            self.subplots["bottom"].set_xlabel(axis_label, position=(1.0, 0.0),
                                               fontsize=fontsize, va="top", ha="right")
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

    def set_axis_max(self, axis_name, maximum):
        if axis_name in self.axis_ranges:
            self.axis_ranges[axis_name] = (self.axis_ranges[axis_name][0], maximum)
        if axis_name == "x":
            self.subplots["top"].set_xlim(right=maximum)
            self.subplots["bottom"].set_xlim(right=maximum)
        elif axis_name == "y":
            self.subplots["top"].set_ylim(top=maximum)
        elif axis_name == "y_ratio":
            self.subplots["bottom"].set_ylim(top=maximum)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_min(self, axis_name, minimum):
        if axis_name in self.axis_ranges:
            self.axis_ranges[axis_name] = (minimum, self.axis_ranges[axis_name][1])
        if axis_name == "x":
            self.subplots["top"].set_xlim(left=minimum)
            self.subplots["bottom"].set_xlim(left=minimum)
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

    def set_axis_ticks(self, axis_name, ticks):
        if axis_name == "x":
            self.subplots["top"].xaxis.set_major_locator(FixedLocator(ticks))
        elif axis_name == "y":
            self.subplots["top"].yaxis.set_major_locator(FixedLocator(ticks))
        elif axis_name == "y_ratio":
            self.subplots["bottom"].yaxis.set_major_locator(FixedLocator(ticks))
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_title(self, title):
        self.subplots["top"].set_title(title)
