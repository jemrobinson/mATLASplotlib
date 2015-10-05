from base_plottable import BasePlottable
# import numpy as np
# from matplotlib import __version__ as mpl_version
import matplotlib.pyplot as pyplot

class Histogram2D(BasePlottable) :
  '''Plottable 2-dimensional histogram, binned along the x and y axes'''
  def __init__( self, *args, **kwargs ) :
    super(Histogram2D, self).__init__( *args, **kwargs )


  ## Add to canvas
  def draw_on_plot( self, axes, **kwargs ) :
    plot_style = kwargs.pop( 'style', None )
    if 'colour_map' in kwargs :
      kwargs['cmap'] = getattr( pyplot.cm, kwargs.pop('colour_map') )
    colourbar_kwargs = {}
    for key in kwargs.keys() :
      if 'colourbar' in key : colourbar_kwargs[key.replace('colourbar_','')] = kwargs.pop(key)

    if plot_style == 'colourbar' :
      data_array, xedges, yedges, image = axes.hist2d( self.x_points, self.y_points, weights=self.z_points, bins=(self.x_bin_edges,self.y_bin_edges), **kwargs )
      axes_image = axes.imshow( data_array, extent=(yedges[0], yedges[-1], xedges[0], xedges[-1]), aspect='auto', **kwargs )
      colourbar = axes.get_figure().colorbar( axes_image, ax=axes, **colourbar_kwargs )
    else :
      raise NotImplementedError( 'Style "{0}" not recognised by {1}'.format( plot_style, type(self) ) )
