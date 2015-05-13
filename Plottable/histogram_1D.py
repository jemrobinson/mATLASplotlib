from base_plottable import BasePlottable
import numpy as np

class Histogram1D(BasePlottable) :
  '''Plottable 1-dimensional histogram, binned along the x-axis'''
  def __init__( self, *args, **kwargs ) :
    super(Histogram1D, self).__init__( *args, **kwargs )


  # Constructor
  def construct_from_values_errors( self, x_values=None, x_error_pairs=None, y_values=None, y_error_pairs=None ) :
    if x_values is None or x_error_pairs is None or y_values is None or y_error_pairs is None :
      self.x_points = np.array([])
      self.y_error_pairs = np.array([])
      self.y_points = np.array([])
      self.y_error_pairs = np.array([])
    else :
      self.x_points = np.array( x_values )
      self.x_error_pairs = np.array( x_error_pairs )
      self.y_points = np.array( y_values )
      self.y_error_pairs = np.array( y_error_pairs )
    assert(self.x_points.size == len( self.x_error_pairs ) == self.y_points.size == len( self.y_error_pairs ) )


  # Plotting behaviour
  def draw_on_plot( self, axes, **kwargs ) :
    plot_style = kwargs.pop( 'style', None )
    kwargs['label'] = kwargs.pop('label',None)
    kwargs['color'] = kwargs.pop('colour_primary','black')
    kwargs['linewidth'] = kwargs.pop('linewidth',2)
    kwargs['linestyle'] = kwargs.pop('linestyle','solid')
    # Remove unused parameters
    kwargs.pop('colour_secondary',kwargs['color'])
    kwargs.pop('hatch',None)
    # Set custom dash styling
    width = kwargs.get('linewidth',1)
    if kwargs['linestyle'] is 'dashed'  : kwargs['dashes'] = ( 3*width,1*width )
    if kwargs['linestyle'] is 'dotted'  : kwargs['dashes'] = ( 1*width,1*width )
    if kwargs['linestyle'] is 'dashdot' : kwargs['dashes'] = ( 2*width,1*width,1*width,1*width )

    if plot_style.startswith('point') :
      kwargs['marker'] = kwargs.pop( 'marker', 'o' ) # Set marker to dot if not set
      if 'xerror' in plot_style : kwargs['xerr'] = np.transpose( self.x_error_pairs )
      if 'yerror' in plot_style : kwargs['yerr'] = np.transpose( self.y_error_pairs )
      # Get error cap sizes
      with_error_bar_caps = kwargs.pop( 'with_error_bar_caps', False )
      kwargs['capthick'] = [0,kwargs.get('linewidth')][with_error_bar_caps]
      kwargs['capsize'] = [0,2*kwargs.get('linewidth')][with_error_bar_caps]
      # Disable linestyle
      kwargs['linestyle'] = 'None'
      axes.errorbar( self.x_points, self.y_points, fmt='', **kwargs )
    elif plot_style == 'join centres' :
      axes.plot( self.x_points, self.y_points, **kwargs )
    elif plot_style == 'stepped line' :
      x_bin_edges = np.array( sum([ [ x_centre - x_errors[0], x_centre + x_errors[1] ] for x_centre, x_errors in zip(self.x_points, self.x_error_pairs) ], [] ) )
      y_bin_edges = np.array( sum([ [ y_centre, y_centre ] for y_centre in self.y_points ], [] ) )
      axes.plot( x_bin_edges, y_bin_edges, drawstyle='steps', **kwargs )
    else :
      raise NotImplementedError( 'Style "{0}" not recognised by {1}'.format( plot_style, type(self) ) )
