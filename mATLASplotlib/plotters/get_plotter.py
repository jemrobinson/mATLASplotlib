"""This module provides the ``get_plotter()`` convenience function."""

from bar_chart import BarChart
from binned_band import BinnedBand
from coloured_2D import Coloured2D
from line import Line
from scatter import Scatter
from stack import Stack


def get_plotter(plot_style):
    """Convert a plot style argument into a concrete class inheriting from BasePlotter.

    :param plot_style: which plot style to use.
    :type plot_style: str
    :return: instantiated plotter object
    :rtype: BasePlotter
    :raises ValueError: No plot style provided.
    :raises NotImplementedError: Unsupported plot style provided.
    """
    if plot_style is None:
        raise ValueError("Plotting style must be provided!")
    if "bar" in plot_style:
        return BarChart(plot_style)
    if "binned band" in plot_style:
        return BinnedBand(plot_style)
    if "coloured 2D" in plot_style:
        return Coloured2D(plot_style)
    if "line" in plot_style:
        return Line(plot_style)
    if "scatter" in plot_style:
        return Scatter(plot_style)
    if "stack" in plot_style:
        return Stack(plot_style)
    raise NotImplementedError("Plotting style '{}' is not supported".format(plot_style))
