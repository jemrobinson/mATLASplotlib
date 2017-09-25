from base_plotter import BasePlotter
import logging
import matplotlib.pyplot as pyplot

logger = logging.getLogger("mATLASplotlib.plotters")

class Coloured2D(BasePlotter):
    """Plot as points in the x-y plane"""
    def __init__(self, plot_style):
        """Constructor."""
        super(Coloured2D, self).__init__(plot_style)

    # Add to canvas
    def add_to_axes(self, axes, dataset, **kwargs):
        # Construct plotting arguments
        self.plot_args["cmap"] = getattr(pyplot.cm, kwargs.pop("colour_map", "Purples")) # Default colour-map: Purples
        # Add any other user-provided arguments
        self.plot_args.update(kwargs)
        # colourbar_kwargs = {}
        # for key in kwargs.keys():
        #     if 'colourbar' in key:
        #         colourbar_kwargs[key.replace('colourbar_', '')] = kwargs.pop(key)
        #
        # if plot_style == 'colourbar':
        x_values, y_values = dataset.unroll_bins(axes="xy")
        assert(len(x_values) == len(y_values) == len(dataset.z_points))
        # Draw with imshow to get the colourbar
        # z_values_array, _xedges, _yedges = np.histogram2d( x_values, y_values, bins=[self.x_bin_edges,self.y_bin_edges], weights=self.z_points )
        # axes_image = axes.imshow( z_values_array, extent=(_yedges[0], _yedges[-1], _xedges[0], _xedges[-1]), aspect='auto', interpolation='nearest', **kwargs )
        z_values_array, _xedges, _yedges, axes_image = axes.hist2d(x_values, y_values, bins=[dataset.x_bin_edges, dataset.y_bin_edges], weights=dataset.z_points, **self.plot_args)
        colourbar = axes.get_figure().colorbar(axes_image, ax=axes, **self.plot_args)
        colourbar.solids.set_rasterized(True)
