from line import Line
from scatter import Scatter
from stack import Stack

def get_plotter(plot_style):
    if "line" in plot_style:
        return Line(plot_style)
    if "scatter" in plot_style:
        return Scatter(plot_style)
    if "stack" in plot_style:
        return Stack(plot_style)
