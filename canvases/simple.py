from base_canvas import BaseCanvas


class Simple(BaseCanvas):
    """Simple canvas with standard ATLAS setup"""
    def __init__(self, shape="square", **kwargs):
        n_pixels, axis_dimensions = (600, 600), [0.15, 0.1, 0.8, 0.85]
        if shape == "rectangular": n_pixels, axis_dimensions = (800, 600), [0.12, 0.1, 0.85, 0.85]
        super(Simple, self).__init__(n_pixels, **kwargs)
        self.subplots["main"] = self.figure.add_axes(axis_dimensions)
        self.main_subplot = "main"

    def _finalise(self):
        if "x" in self.axis_ranges:
            self.subplots["main"].set_xlim(self.axis_ranges["x"])
        if "y" in self.axis_ranges:
            self.subplots["main"].set_ylim(self.axis_ranges["y"])

    # Axis labels
    def get_axis_label(self, axis_name):
        if axis_name == "x":
            return self.subplots["main"].get_xlabel()
        elif axis_name == "y":
            return self.subplots["main"].get_ylabel()
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_label(self, axis_name, axis_label):
        if axis_name == "x":
            self.subplots["main"].set_xlabel(axis_label, size=16, position=(1.0, 0.0), va="top", ha="right")
        elif axis_name == "y":
            self.subplots["main"].set_ylabel(axis_label, size=16)
            self.subplots["main"].yaxis.get_label().set_ha("right")
            self.subplots["main"].yaxis.set_label_coords(-0.13, 1.0)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_labels(self, x_axis_label, y_axis_label):
        self.set_axis_label("x", x_axis_label)
        self.set_axis_label("y", y_axis_label)

    # Axis ranges
    def set_axis_range(self, axis_name, axis_range):
        if axis_name == "x":
            self.axis_ranges["x"] = axis_range
        elif axis_name == "y":
            self.axis_ranges["y"] = axis_range
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_ranges(self, x_axis_range, y_axis_range):
        self.set_axis_range("x", x_axis_range)
        self.set_axis_range("y", y_axis_range)

    # Plot title
    def set_title(self, title):
        self.subplots["main"].set_title(title)
