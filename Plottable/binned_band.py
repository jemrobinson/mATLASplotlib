from base_plottable import BasePlottable

class BinnedBand(BasePlottable) :
  '''Plottable band, binned along the x-axis'''
  def __init__( self, x_bin_edges=None, y_values=None, y_error_pairs=None ) :
      self.__construct__( x_bin_edges, y_values, y_error_pairs )

  def __construct__( self, x_values, x_errors, y_values, y_errors ) :
    if x_bin_edges is not None and y_values is not None and  y_error_pairs is not None :
      x_centres = [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( x_bin_edges[:-1], x_bin_edges[1:] ) ]
      x_errors = [ centre-low_edge for centre, low_edge in zip(x_centres,x_bin_edges[:-1]) ]

      self.x_points = sum([ [val-err,val+err] for val,err in zip( x_centres, x_errors ) ], [] )
      self.y_points_l = sum([ [val-err[0],val-err[0]] for val,err in zip( y_values, y_error_pairs ) ], [])
      self.y_points_h = sum([ [val+err[1],val+err[1]] for val,err in zip( y_values, y_error_pairs ) ], [])
    else :
      self.x_points = []
      self.y_points_l = []
      self.y_points_h = []

    assert( len(self.x_points) == len(self.y_points_l) == len(self.y_points_h) )

  def draw_on_plot( self, plot, **kwargs ) :
    plot_style = kwargs.get( 'style', None )
    plot_label = kwargs.get( 'label', None )
    plot_colour_primary = kwargs.get( 'colour_primary', 'black' )
    plot_colour_secondary = kwargs.get( 'colour_secondary', 'black' )
    plot_hatch_style = kwargs.get( 'hatch', None )
    plot_alpha = kwargs.get( 'alpha', None )

    if plot_style == 'filled_band' :
      if plot_label == None :
        plot.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
      else :
        plot.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
        self.fill_between_proxy( (0.0,0.0), (0.0,0.0), (0.0,0.0), axes=plot, label=text, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha )
        print self.x_points, self.y_points_l, self.y_points_h, plot_colour_primary, plot_colour_secondary, plot_hatch_style, plot_alpha

  def fill_between_proxy( self, x, y1, y2, axes=None, **kwargs):
    axes = axes if axes is not None else plt.gca()
    axes.fill_between(x, y1, y2, **kwargs)
    proxy_artist = plt.Rectangle((0, 0), 0, 0, **kwargs)
    axes.add_patch(proxy_artist)
    return proxy_artist

  def number_of_points( self ) :
    return len(self.x_points)

