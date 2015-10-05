from base_plottable import BasePlottable
import matplotlib.pyplot as pyplot
import numpy as np
from . import Histogram1D

class Scatter2D(BasePlottable) :
  '''Two-dimensional scatter plot'''
  def __init__( self, *args, **kwargs ) :
    super(Scatter2D, self).__init__( *args, **kwargs )


  # Constructor
  def construct_from_values_errors( self, x_values=None, x_error_pairs=None, y_values=None, y_error_pairs=None ) :
    if x_values is None or x_error_pairs is None or y_values is None or y_error_pairs is None :
      self.x_points = np.array([])
      self.y_points = np.array([])
      self.y_error_centres = np.array([])
      self.y_error_sizes = np.array([])
    else :
      self.x_points = np.array( x_values )
      self.x_error_centres = np.array( [ value+(errors[1]-errors[0])/2.0 for value, errors in zip( x_values, x_error_pairs ) ] )
      self.x_error_sizes = np.array( [ (errors[0]+errors[1])/2.0 for errors in x_error_pairs ] )
      self.y_points = np.array( y_values )
      self.y_error_centres = np.array( [ value+(errors[1]-errors[0])/2.0 for value, errors in zip( y_values, y_error_pairs ) ] )
      self.y_error_sizes = np.array( [ (errors[0]+errors[1])/2.0 for errors in y_error_pairs ] )
    assert( self.x_points.size == self.x_error_centres.size == self.x_error_sizes.size == self.y_points.size == self.y_error_centres.size == self.y_error_sizes.size )


  # Plotting behaviour
  def draw_on_plot( self, axes, **kwargs ) :
    plot_style = kwargs.pop( 'style', None )
    plot_label = kwargs.pop( 'label', None )
    plot_linestyle = kwargs.pop('linestyle',None)
    plot_marker = kwargs.pop( 'marker', '.' )
    plot_colour_primary = kwargs.pop( 'colour_primary', 'black' )
    plot_colour_secondary = kwargs.pop( 'colour_secondary', 'none' )
    plot_with_error_bar_caps = kwargs.pop( 'with_error_bar_caps', False )

    if 'scatter' in plot_style  :
      if 'yerror' in plot_style :
        hist1D = Histogram1D( self.x_error_centres, self.x_error_sizes, self.y_error_centres, self.y_error_sizes )
        hist1D.draw_on_plot( axes, marker=None, style='point yerror', colour_primary=plot_colour_primary, linestyle=plot_linestyle )
      axes.scatter( self.x_points, self.y_points, label=plot_label, facecolors=plot_colour_primary, edgecolors=plot_colour_secondary, marker=plot_marker, **kwargs )
    else :
      raise NotImplementedError( 'Style "{0}" not recognised by {1}'.format( plot_style, type(self) ) )
