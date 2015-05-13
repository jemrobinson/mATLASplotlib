from base_plottable import BasePlottable
import matplotlib.pyplot as pyplot
import numpy as np

class BinnedBand(BasePlottable) :
  '''Plottable band, binned along the x-axis'''
  def __init__( self, x_values=None, x_error_pairs=None, y_values=None, y_error_pairs=None ) :
    super(BinnedBand, self).__init__( 'BinnedBand' )
    if x_values is None or x_error_pairs is None or y_values is None or y_error_pairs is None :
      self.x_points = np.array([])
      self.y_points_l = np.array([])
      self.y_points_h = np.array([])
    else :
      self.x_points = np.array( sum([ [value-errors[0],value+errors[1]] for value,errors in zip( x_values, x_error_pairs ) ], [] ) )
      self.y_points_l = np.array( sum([ [value-errors[0],value-errors[0]] for value,errors in zip( y_values, y_error_pairs ) ], [] ) )
      self.y_points_h = np.array( sum([ [value+errors[1],value+errors[1]] for value,errors in zip( y_values, y_error_pairs ) ], [] ) )
    assert( self.x_points.size == self.y_points_l.size == self.y_points_h.size )


  def draw_on_plot( self, axes, **kwargs ) :
    plot_style = kwargs.get( 'style', None )
    plot_label = kwargs.get( 'label', None )
    plot_colour_primary = kwargs.get( 'colour_primary', 'black' )
    plot_colour_secondary = kwargs.get( 'colour_secondary', 'black' )
    plot_hatch_style = kwargs.get( 'hatch', None )
    plot_alpha = kwargs.get( 'alpha', None )

    if plot_style == 'filled band' :
      if plot_label == None :
        axes.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
      else :
        axes.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
        proxy_artist = pyplot.Rectangle( (0,0), 0, 0, axes=axes, label=plot_label, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
        axes.add_patch( proxy_artist )
    else :
      raise NotImplementedError( 'Style "{0}" not recognised by {1}'.format( plot_style, type(self) ) )
