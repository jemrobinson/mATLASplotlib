from base_plottable import BasePlottable
# import matplotlib.pyplot as pyplot
import numpy as np

class Histogram1D(BasePlottable) :
  '''Plottable 1-dimensional histogram, binned along the x-axis'''
  def __init__( self, x_values=None, x_error_pairs=None, y_values=None, y_error_pairs=None ) :
    super(Histogram1D, self).__init__( 'Histogram1D' )
    if x_values is None or x_error_pairs is None or y_values is None or y_error_pairs is None :
      self.x_points = np.array([])
      self.y_error_pairs = np.array([])
      self.y_points = np.array([])
      self.y_error_pairs = np.array([])
    else :
      self.x_points = np.array( x_values )
      self.x_error_pairs = np.array( x_error_pairs )
      self.y_points = np.array( y_values )
      self.y_error_pairs = np.array( y_error_pairs ) #[ (err[0],err[1]) for err in y_error_pairs ] )
    assert(self.x_points.size == len( self.x_error_pairs ) == self.y_points.size == len( self.y_error_pairs ) )

  def draw_on_plot( self, plot, **kwargs ) :
    plot_style = kwargs.get( 'style', None )
    plot_label = kwargs.get( 'label', None )
    plot_colour_primary = kwargs.get( 'colour_primary', 'black' )
    plot_marker = kwargs.get( 'marker', 'o' )

    if plot_style.startswith('point') :
      kwargs = {}
      if 'xerror' in plot_style : kwargs['xerr'] = np.transpose( self.x_error_pairs )
      if 'yerror' in plot_style : kwargs['yerr'] = np.transpose( self.y_error_pairs )

      # plot.errorbar( self.x_points, self.y_points, yerr=np.transpose( self.y_error_pairs ), fmt=plot_marker, color=plot_colour_primary )
      plot.errorbar( self.x_points, self.y_points, fmt=plot_marker, color=plot_colour_primary, **kwargs )



    elif plot_style == 'join centres' :
      plot.plot( self.x_points, self.y_points )

    elif plot_style == 'stepped line' :
      x_bin_edges = np.array( [ (x_centre - x_errors[0]) for x_centre, x_errors in zip(self.x_points, self.x_error_pairs) ] + [ self.x_points[-1]+self.x_error_pairs[-1][1] ] )
      plot.hist( self.x_points, bins=x_bin_edges, weights=self.y_points, histtype='step' )


      # print values, bin_edges
      # if plot_label == None :
      #   plot.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
      #   print self.x_points, self.y_points_l, self.y_points_h, plot_colour_primary, plot_colour_secondary, plot_hatch_style, plot_alpha
      # else :
      #   plot.fill_between( self.x_points, self.y_points_l, self.y_points_h, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha, linewidth=0 )
      #   self.fill_between_proxy( (0.0,0.0), (0.0,0.0), (0.0,0.0), axes=plot, label=text, facecolor=plot_colour_primary, edgecolor=plot_colour_secondary, hatch=plot_hatch_style, alpha=plot_alpha )
      #   print self.x_points, self.y_points_l, self.y_points_h, plot_colour_primary, plot_colour_secondary, plot_hatch_style, plot_alpha
    else :
      raise NotImplementedError( 'Style {0} not recognised by {1}'.format( plot_style, type(self) ) )
