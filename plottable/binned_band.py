# from base_plottable import BasePlottable
# import matplotlib.pyplot as pyplot


# class BinnedBand(BasePlottable):
#     '''Plottable band, binned along the x-axis'''

#     def __init__(self, *args, **kwargs):
#         super(BinnedBand, self).__init__(*args, **kwargs)

#     # Add to canvas
#     def draw_on_plot(self, axes, **kwargs):
#         plot_style = kwargs.get('style', None)
#         plot_label = kwargs.get('label', None)
#         plot_colour_primary = kwargs.get('colour_primary', 'black')
#         plot_colour_secondary = kwargs.get('colour_secondary', 'black')
#         plot_hatch_style = kwargs.get('hatch', None)
#         plot_alpha = kwargs.get('alpha', None)

#         if plot_style == 'filled band':
#             if plot_label == None:
#                 axes.fill_between(self.band_edges_x, self.band_edges_y_low, self.band_edges_y_high, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0)
#             else:
#                 axes.fill_between(self.band_edges_x, self.band_edges_y_low, self.band_edges_y_high, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0)
#                 proxy_artist = pyplot.Rectangle((0, 0), 0, 0, axes=axes, label=plot_label, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0)
#                 axes.add_patch(proxy_artist)
#         else:
#             raise NotImplementedError('Style "{0}" not recognised by {1}'.format(plot_style, type(self)))
