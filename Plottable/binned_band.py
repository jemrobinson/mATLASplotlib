from base_plottable import BasePlottable
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


  def draw_on_plot( self, plot, **kwargs ) :
    plot_style = kwargs.get( 'style', None )
    plot_label = kwargs.get( 'label', None )
    plot_colour_primary = kwargs.get( 'colour_primary', 'black' )
    plot_colour_secondary = kwargs.get( 'colour_secondary', 'black' )
    plot_hatch_style = kwargs.get( 'hatch', None )
    plot_alpha = kwargs.get( 'alpha', None )

    if plot_style == 'filled band' :
      if plot_label == None :
        plot.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
      else :
        plot.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
        self.fill_between_proxy( (0.0,0.0), (0.0,0.0), (0.0,0.0), axes=plot, label=text, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha )
    else :
      raise NotImplementedError( 'Style {0} not recognised by {1}'.format( plot_style, type(self) ) )

  def fill_between_proxy( self, x, y1, y2, axes=None, **kwargs):
    axes = axes if axes is not None else plt.gca()
    axes.fill_between(x, y1, y2, **kwargs)
    proxy_artist = plt.Rectangle((0, 0), 0, 0, **kwargs)
    axes.add_patch(proxy_artist)
    return proxy_artist

  def number_of_points( self ) :
    return len(self.x_points)

