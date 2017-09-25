# from base_plottable import BasePlottable
# import matplotlib.pyplot as pyplot
# import numpy as np


# class Histogram2D(BasePlottable):
#     '''Plottable 2-dimensional histogram, binned along the x and y axes'''

#     def __init__(self, *args, **kwargs):
#         super(Histogram2D, self).__init__(*args, **kwargs)

#     # Add to canvas
#     def draw_on_plot(self, axes, **kwargs):
#         plot_style = kwargs.pop('style', None)
#         if 'colour_map' in kwargs:
#             kwargs['cmap'] = getattr(pyplot.cm, kwargs.pop('colour_map'))
#         colourbar_kwargs = {}
#         for key in kwargs.keys():
#             if 'colourbar' in key:
#                 colourbar_kwargs[key.replace('colourbar_', '')] = kwargs.pop(key)

#         if plot_style == 'colourbar':
#             x_values, y_values = self.unroll_bins(self.x_points, self.y_points)
#             assert(len(x_values) == len(y_values) == len(self.z_points))
#             # Draw with imshow to get the colourbar
#             # z_values_array, _xedges, _yedges = np.histogram2d( x_values, y_values, bins=[self.x_bin_edges,self.y_bin_edges], weights=self.z_points )
#             # axes_image = axes.imshow( z_values_array, extent=(_yedges[0], _yedges[-1], _xedges[0], _xedges[-1]), aspect='auto', interpolation='nearest', **kwargs )
#             z_values_array, _xedges, _yedges, axes_image = axes.hist2d(x_values, y_values, bins=[self.x_bin_edges, self.y_bin_edges], weights=self.z_points, **kwargs)
#             colourbar = axes.get_figure().colorbar(axes_image, ax=axes, **colourbar_kwargs)
#             colourbar.solids.set_rasterized(True)
#         else:
#             raise NotImplementedError('Style "{0}" not recognised by {1}'.format(plot_style, type(self)))
