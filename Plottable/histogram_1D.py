from base_plottable import BasePlottable

class Histogram1D(BasePlottable) :
  '''Plottable 1-dimensional histogram, binned along the x-axi'''
  def __init__( self, x_bin_edges=None, y_values=None, y_error_pairs=None ) :
    self.__construct__( x_bin_edges, y_values, y_error_pairs )

  def __construct__( self, x_bin_edges, y_values, y_errors ) :
    if x_bin_edges is not None and y_values is not None and  y_error_pairs is not None :
      self.x_points = [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( x_bin_edges[:-1], x_bin_edges[1:] ) ]
      self.x_errors = [ centre-low_edge for centre, low_edge in zip(x_centres,x_bin_edges[:-1]) ]
      self.y_values = y_values
      self.y_errors = y_errors
    else :
      self.x_points, self.x_errors = [], []
      self.y_values, self.y_errors = [], []

    assert( len(self.x_points) == len(self.y_values) == len(self.y_errors) )

  def from_TH1( self, input_TH1 ) :
    x_bin_edges = [ input_TH1.GetBinLowEdge(bin) for bin in range(1,input_TH1.GetNbinsX()+2) ]
    y_values = [ input_TH1.GetBinContent(bin) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    y_error_pairs = [ (input_TH1.GetBinError(bin),input_TH1.GetBinError(bin)) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    self.__construct__( x_bin_edges, y_values, y_error_pairs )


  # def draw_on_plot( self, plot, **kwargs ) :
  #   plot_style = kwargs.get( 'style', None )
  #   plot_label = kwargs.get( 'label', None )
  #   plot_colour_primary = kwargs.get( 'colour_primary', 'black' )
  #   plot_colour_secondary = kwargs.get( 'colour_secondary', 'black' )
  #   plot_hatch_style = kwargs.get( 'hatch', None )
  #   plot_alpha = kwargs.get( 'alpha', None )

  #   if plot_style == 'filled_band' :
  #     # band_points = self.get_envelope_points( hist )
  #     # kwargs['linewidth'] = 0
  #     # self.plots[plot].set_rasterization_zorder(1) # http://osxastrotricks.wordpress.com/2014/01/19/rasterized-graphics-with-matplotlib-to-preserve-plot-transparencies-for-apj-figures/ %, zorder=0
  #     if plot_label == None :
  #       print len( self.x_points ), len(self.y_points_l), len(self.y_points_h)
  #       plot.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
  #       print self.x_points, self.y_points_l, self.y_points_h, plot_colour_primary, plot_colour_secondary, plot_hatch_style, plot_alpha

  #     else :
  #       # self.fill_between_proxy( band_points[0], band_points[1], band_points[2], axes=self.plots[plot], label=text, facecolor=maincolour, edgecolor=secondcolour, hatch=hatch, alpha=alpha, **kwargs )
  #       # # Also draw central line if this is appearing on a legend
  #       # self.add_to_plot( hist.nominal, plot=plot, style='line', label=None, xerr=xerr, colour=maincolour, linewidth=2, alpha=alpha )
  #       # print plot, text, maincolour, secondcolour, hatch, alpha, kwargs

  #       # hatch=hatch
  #       plot.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
  #       self.fill_between_proxy( (0.0,0.0), (0.0,0.0), (0.0,0.0), axes=plot, label=text, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha )
  #       print self.x_points, self.y_points_l, self.y_points_h, plot_colour_primary, plot_colour_secondary, plot_hatch_style, plot_alpha

  # def fill_between_proxy( self, x, y1, y2, axes=None, **kwargs):
  #   axes = axes if axes is not None else plt.gca()
  #   axes.fill_between(x, y1, y2, **kwargs)
  #   proxy_artist = plt.Rectangle((0, 0), 0, 0, **kwargs)
  #   axes.add_patch(proxy_artist)
  #   return proxy_artist
