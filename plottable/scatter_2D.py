from base_plottable import BasePlottable
import matplotlib.pyplot as pyplot
import numpy as np
from . import Histogram1D


class Scatter2D(BasePlottable):
    '''Two-dimensional scatter plot'''

    def __init__(self, *args, **kwargs):
        super(Scatter2D, self).__init__(*args, **kwargs)

    # Add to canvas
    def draw_on_plot(self, axes, **kwargs):
        plot_style = kwargs.pop('style', None)
        plot_label = kwargs.pop('label', None)
        plot_linestyle = kwargs.pop('linestyle', None)
        plot_marker = kwargs.pop('marker', 'o')
        plot_marker_size = kwargs.pop('markersize', '20')
        plot_colour_primary = kwargs.pop('colour_primary', 'black')
        plot_colour_secondary = kwargs.pop('colour_secondary', 'none')
        plot_with_error_bar_caps = kwargs.pop('with_error_bar_caps', False)

        if 'scatter' in plot_style:
            if 'yerror' in plot_style:
                hist1D = Histogram1D(self.x_points_error_symmetrised, self.x_errors_symmetrised, self.y_points_error_symmetrised, self.y_errors_symmetrised)
                hist1D.draw_on_plot(axes, marker=None, style='point yerror', colour_primary=plot_colour_primary, linestyle=plot_linestyle)
            axes.scatter(self.x_points, self.y_points, marker=plot_marker, s=plot_marker_size, label=plot_label, facecolors=plot_colour_primary, edgecolors=plot_colour_secondary, **kwargs)
        else:
            raise NotImplementedError('Style "{0}" not recognised by {1}'.format(plot_style, type(self)))
