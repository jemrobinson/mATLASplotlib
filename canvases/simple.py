from base_canvas import BaseCanvas
from matplotlib.ticker import FixedLocator


class Simple(BaseCanvas):
    """Simple canvas with standard ATLAS setup."""

    def __init__(self, shape="square", **kwargs):
        """Constructor."""
        shape_dict = {"square": {"n_pixels": (600, 600), "dimensions": (0.15, 0.1, 0.8, 0.85), "y_label_offset": -0.13},
                      "rectangular": {"n_pixels": (800, 600), "dimensions": (0.12, 0.1, 0.85, 0.85), "y_label_offset": -0.0975}}
        self.shape_dict = shape_dict[shape]
        super(Simple, self).__init__(self.shape_dict["n_pixels"], **kwargs)
        self.subplots["main"] = self.figure.add_axes(self.shape_dict["dimensions"])
        self.main_subplot = "main"

    def _finalise(self):
        if "x" in self.axis_ranges:
            self.subplots["main"].set_xlim(self.axis_ranges["x"])
        if "y" in self.axis_ranges:
            self.subplots["main"].set_ylim(self.axis_ranges["y"])

    def get_axis_label(self, axis_name):
        """Get axis labels."""
        if axis_name == "x":
            return self.subplots["main"].get_xlabel()
        elif axis_name == "y":
            return self.subplots["main"].get_ylabel()
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_label(self, axis_name, axis_label):
        """Set axis labels."""
        if axis_name == "x":
            self.subplots["main"].set_xlabel(axis_label, size=16, position=(1.0, 0.0), va="top", ha="right")
        elif axis_name == "y":
            self.subplots["main"].set_ylabel(axis_label, size=16)
            self.subplots["main"].yaxis.get_label().set_ha("right")
            self.subplots["main"].yaxis.set_label_coords(self.shape_dict["y_label_offset"], 1.0)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_labels(self, x_axis_label, y_axis_label):
        """Document here."""
        self.set_axis_label("x", x_axis_label)
        self.set_axis_label("y", y_axis_label)

    # Axis ranges
    def set_axis_max(self, axis_name, maximum):
        if axis_name == "x":
            self.subplots["main"].set_xlim(top=maximum)
        elif axis_name == "y":
            self.subplots["main"].set_ylim(top=maximum)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_min(self, axis_name, minimum):
        if axis_name == "x":
            self.subplots["main"].set_xlim(bottom=minimum)
        elif axis_name == "y":
            self.subplots["main"].set_ylim(bottom=minimum)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_range(self, axis_name, axis_range):
        """Document here."""
        if axis_name == "x":
            self.axis_ranges["x"] = axis_range
        elif axis_name == "y":
            self.axis_ranges["y"] = axis_range
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_ranges(self, x_axis_range, y_axis_range):
        """Document here."""
        self.set_axis_range("x", x_axis_range)
        self.set_axis_range("y", y_axis_range)

    def set_axis_ticks(self, axis_name, ticks):
        """Document here."""
        if axis_name == "x":
            self.subplots["main"].xaxis.set_major_locator(FixedLocator(ticks))
        elif axis_name == "y":
            self.subplots["main"].yaxis.set_major_locator(FixedLocator(ticks))
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    # Plot title
    def set_title(self, title):
        """Document here."""
        self.subplots["main"].set_title(title)
