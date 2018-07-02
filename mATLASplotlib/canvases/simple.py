""" This module provides the ``Simple`` canvas."""
from matplotlib.ticker import FixedLocator
from base_canvas import BaseCanvas


class Simple(BaseCanvas):
    """Simple canvas with standard ATLAS setup."""

    def __init__(self, shape="square", **kwargs):
        shape_dict = {"square": {"dimensions": (0.15, 0.1, 0.8, 0.85), "y_label_offset": -0.13},
                      "landscape": {"dimensions": (0.12, 0.1, 0.84, 0.85), "y_label_offset": -0.0975}}
        self.shape_dict = shape_dict[shape]
        super(Simple, self).__init__(shape=shape, **kwargs)
        self.subplots["main"] = self.figure.add_axes(self.shape_dict["dimensions"])
        self.main_subplot = "main"

    def plot_dataset(self, *args, **kwargs):
        axes = kwargs.get("axes", self.main_subplot)
        super(Simple, self).plot_dataset(*args, **kwargs)
        if "x" not in self.axis_ranges:
            self.set_axis_range("x", self.subplots[axes].get_xlim())
        if "y" not in self.axis_ranges:
            self.set_axis_range("y", self.subplots[axes].get_ylim())

    def _apply_axis_limits(self):
        if "x" in self.axis_ranges:
            self.subplots["main"].set_xlim(self.axis_ranges["x"])
        if "y" in self.axis_ranges:
            self.subplots["main"].set_ylim(self.axis_ranges["y"])

    def get_axis_label(self, axis_name):
        if axis_name == "x":
            return self.subplots["main"].get_xlabel()
        elif axis_name == "y":
            return self.subplots["main"].get_ylabel()
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_label(self, axis_name, axis_label, fontsize=16):
        if axis_name == "x":
            self.subplots["main"].set_xlabel(axis_label, fontsize=fontsize, position=(1.0, 0.0), va="top", ha="right")
        elif axis_name == "y":
            self.subplots["main"].set_ylabel(axis_label, fontsize=fontsize)
            self.subplots["main"].yaxis.get_label().set_ha("right")
            self.subplots["main"].yaxis.set_label_coords(self.shape_dict["y_label_offset"], 1.0)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    # Axis ranges
    def set_axis_max(self, axis_name, maximum):
        if axis_name in self.axis_ranges:
            self.axis_ranges[axis_name] = (self.axis_ranges[axis_name][0], maximum)
        if axis_name == "x":
            self.subplots["main"].set_xlim(right=maximum)
        elif axis_name == "y":
            self.subplots["main"].set_ylim(top=maximum)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_min(self, axis_name, minimum):
        if axis_name in self.axis_ranges:
            self.axis_ranges[axis_name] = (minimum, self.axis_ranges[axis_name][1])
        if axis_name == "x":
            self.subplots["main"].set_xlim(left=minimum)
        elif axis_name == "y":
            self.subplots["main"].set_ylim(bottom=minimum)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_range(self, axis_name, axis_range):
        if axis_name == "x":
            self.axis_ranges["x"] = tuple(axis_range)
        elif axis_name == "y":
            self.axis_ranges["y"] = tuple(axis_range)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_ticks(self, axis_name, ticks):
        if axis_name == "x":
            self.subplots["main"].xaxis.set_major_locator(FixedLocator(ticks))
        elif axis_name == "y":
            self.subplots["main"].yaxis.set_major_locator(FixedLocator(ticks))
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_title(self, title):
        self.subplots["main"].set_title(title)
