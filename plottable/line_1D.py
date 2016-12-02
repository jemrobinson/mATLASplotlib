from base_plottable import BasePlottable
# import numpy as np


class Line1D(BasePlottable):
    '''Plottable 1-dimensional histogram, binned along the x-axis'''

    def __init__(self, *args, **kwargs):
        super(Line1D, self).__init__(*args, **kwargs)

    # Add to canvas
    def draw_on_plot(self, axes, **kwargs):
        kwargs['label'] = kwargs.pop('label', None)
        kwargs['linewidth'] = kwargs.pop('linewidth', 2)
        kwargs['color'] = kwargs.pop('colour_primary', 'black')
        kwargs['linestyle'] = kwargs.pop('style', 'solid')

        # Plot simple line with arguments
        axes.plot(self.x_points, self.y_points, **kwargs)
