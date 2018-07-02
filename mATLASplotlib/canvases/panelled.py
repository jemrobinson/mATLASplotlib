""" This module provides the ``Panelled`` canvas."""
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
from base_canvas import BaseCanvas
from ..formatters import force_ndp


class Panelled(BaseCanvas):
    """Panelled canvas with standard ATLAS setup."""

    def __init__(self, shape="portrait", n_panels=3, top_panel_fraction=0.16, **kwargs):
        """Set up Panelled canvas properties.

        The canvas consists of a single top panel and ``n_panels`` equally sized additional panels underneath.
        These additional panels are called ``plot0``, ``plot1``, etc. with the numbering starting from the top.

        :param shape: use either the 'square', 'landscape' or 'portrait' ATLAS proportions
        :type shape: str
        :param n_panels: how many panels to include
        :type n_panels: int
        :param top_panel_fraction: fraction of vertical space that the top panel should use up
        :type top_panel_fraction: float

        :Keyword Arguments: as for :py:class:`.BaseCanvas`
        """
        super(Panelled, self).__init__(shape=shape, **kwargs)
        _margin_top, _margin_bottom = 0.02, 0.08
        self.n_panels = n_panels
        subplot_height = (1.0 - _margin_top - _margin_bottom - top_panel_fraction) / self.n_panels
        self.subplots["top"] = self.figure.add_axes([0.15, 1.0 - _margin_top - top_panel_fraction, 0.8, top_panel_fraction])
        for idx in range(n_panels):
            _panel_limits = [0.15, (1.0 - _margin_top - top_panel_fraction - (idx + 1) * subplot_height), 0.8, subplot_height]
            self.subplots["plot{0}".format(idx)] = self.figure.add_axes(_panel_limits)
            self.axis_ranges["y_plot{0}".format(idx)] = [0.5, 1.5]
        self.use_auto_ratio_ticks = dict((name, True) for name in self.subplots if name != "top")
        self.main_subplot = "plot0"

    def plot_dataset(self, *args, **kwargs):
        subplot_name = kwargs.get("axes", self.main_subplot)
        super(Panelled, self).plot_dataset(*args, **kwargs)
        if "x" not in self.axis_ranges:
            self.set_axis_range("x", self.subplots[subplot_name].get_xlim())
        if "plot" in subplot_name:
            y_axis_name = "y_{0}".format(subplot_name)
            self.set_axis_range(y_axis_name, self.subplots[subplot_name].get_ylim())

    def add_legend(self, x, y, anchor_to="lower left", fontsize=None, axes=None):
        """Add a legend to the canvas at (x, y).

        If added to the ``top`` panel then all elements from the lower panels will be included in it.

        :Arguments: as for :py:meth:`.BaseCanvas.add_legend`
        """
        subplot_name = self.main_subplot if axes is None else axes
        if subplot_name == "top":
            subplots = [self.subplots["plot{0}".format(idx)] for idx in range(self.n_panels)]
            self.legend.plot(x, y, self.subplots[subplot_name], anchor_to, fontsize, use_axes=subplots)
        else:
            self.legend.plot(x, y, self.subplots[subplot_name], anchor_to, fontsize)

    def get_axis_label(self, axis_name):
        if axis_name == "x":
            return self.subplots[self.bottom_panel].get_xlabel()
        elif axis_name == "y":
            return self.subplots["top"].get_ylabel()
        raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_label(self, axis_name, axis_label, fontsize=16):
        if axis_name == "x":
            self.subplots[self.bottom_panel].set_xlabel(axis_label, position=(1.0, 0.0),
                                                        fontsize=fontsize, va="top", ha="right")
        elif axis_name == "y":
            self.subplots["top"].set_ylabel(axis_label, fontsize=fontsize)
            self.subplots["top"].yaxis.get_label().set_ha("right")
            self.subplots["top"].yaxis.set_label_coords(-0.13, 1.0)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_max(self, axis_name, maximum):
        if axis_name in self.axis_ranges:
            self.axis_ranges[axis_name] = (self.axis_ranges[axis_name][0], maximum)
        if axis_name == "x":
            for subplot in self.subplots.values():
                subplot.set_xlim(right=maximum)
        elif axis_name[0] == "y":
            self.subplots[axis_name.replace("y_", "")].set_ylim(top=maximum)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_min(self, axis_name, minimum):
        if axis_name in self.axis_ranges:
            self.axis_ranges[axis_name] = (minimum, self.axis_ranges[axis_name][1])
        if axis_name == "x":
            for subplot in self.subplots.values():
                subplot.set_xlim(left=minimum)
        elif "y_plot" in axis_name:
            self.subplots[axis_name.replace("y_", "")].set_ylim(bottom=minimum)
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_range(self, axis_name, axis_range):
        if axis_name == "x":
            self.axis_ranges["x"] = axis_range
        elif "y_plot" in axis_name:
            self.axis_ranges[axis_name] = axis_range
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_axis_ticks(self, axis_name, ticks):
        if axis_name == "x":
            for subplot in [p for n, p in self.subplots.items() if n != "top"]:
                subplot.xaxis.set_major_locator(FixedLocator(ticks))
        elif "y_plot" in axis_name:
            subplot_name = axis_name.replace("y_", "")
            self.subplots[subplot_name].yaxis.set_major_locator(FixedLocator(ticks))
            self.use_auto_ratio_ticks[subplot_name] = False
        else:
            raise ValueError("axis {0} not recognised by {1}".format(axis_name, type(self)))

    def set_title(self, title):
        self.subplots["top"].set_title(title)

    def _apply_axis_limits(self):
        if "x" in self.axis_ranges:
            for subplot in self.subplots.values():
                subplot.set_xlim(self.axis_ranges["x"])
        for axis_name in self.axis_ranges:
            if "y_plot" in axis_name:
                self.subplots[axis_name.replace("y_", "")].set_ylim(self.axis_ranges[axis_name])

    def _apply_final_formatting(self):
        """Apply final formatting. Remove unnecessary ticks and labels."""
        # Set axis decimal places
        for axis_name, ndp in self.axis_tick_ndps.items():
            if axis_name == "x":
                self.subplots[self.bottom_panel].xaxis.set_major_formatter(FuncFormatter(force_ndp(nplaces=ndp)))
            elif "y_plot" in axis_name:
                self.subplots[axis_name.replace("y_", "")].yaxis.set_major_formatter(FuncFormatter(force_ndp(nplaces=ndp)))

        # Remove x-axis labels from plots
        for subplot in [a for n, a in self.subplots.items() if n != self.bottom_panel]:
            subplot.set_xticklabels([])

        # Set the ratio ticks appropriately
        for subplot_name in [n for n in self.subplots if n != "top"]:
            if self.use_auto_ratio_ticks[subplot_name]:
                axis_name = "y_{0}".format(subplot_name)
                self.set_axis_ticks(axis_name, self._get_auto_axis_ticks(axis_name=axis_name))

        # Remove all tick marks from top plot
        self.subplots["top"].xaxis.set_major_locator(NullLocator())
        self.subplots["top"].yaxis.set_major_locator(NullLocator())
        self.subplots["top"].xaxis.set_minor_locator(NullLocator())
        self.subplots["top"].yaxis.set_minor_locator(NullLocator())

        # Shift y-axis label downwards
        self.subplots["top"].yaxis.set_label_coords(-0.12, 0.3)

    @property
    def bottom_panel(self):
        """Name of the bottom-most panel."""
        return "plot{0}".format(self.n_panels - 1)
