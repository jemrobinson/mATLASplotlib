from base_plottable import BasePlottable
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
      self.y_error_pairs = np.array( y_error_pairs )
    assert(self.x_points.size == len( self.x_error_pairs ) == self.y_points.size == len( self.y_error_pairs ) )

  def draw_on_plot( self, axes, **kwargs ) :
    plot_style = kwargs.get( 'style', None )
    plot_label = kwargs.get( 'label', None )
    plot_colour_primary = kwargs.get( 'colour_primary', 'black' )
    plot_marker = kwargs.get( 'marker', 'o' )
    plotter_kwargs = { 'label':plot_label, 'color':plot_colour_primary, 'linewidth':kwargs.get('linewidth',2) }
    # Set linestyle
    w = plotter_kwargs.get('linewidth',1)
    if kwargs['linestyle'] is 'dashed'  : plotter_kwargs['dashes'] = ( 3*w,1*w )
    if kwargs['linestyle'] is 'dotted'  : plotter_kwargs['dashes'] = ( 1*w,1*w )
    if kwargs['linestyle'] is 'dashdot' : plotter_kwargs['dashes'] = ( 2*w,1*w,1*w,1*w )

    if plot_style.startswith('point') :
      if 'xerror' in plot_style : plotter_kwargs['xerr'] = np.transpose( self.x_error_pairs )
      if 'yerror' in plot_style : plotter_kwargs['yerr'] = np.transpose( self.y_error_pairs )
      axes.errorbar( self.x_points, self.y_points, fmt=plot_marker, capsize=0, **plotter_kwargs )
      # rplt.errorbar( hist, axes=self.plots[plot], xerr=xerr, capsize=0, label=text, marker=markertype, markerfacecolor=markerface, markeredgecolor=maincolour, ecolor=maincolour, markersize=6, **kwargs )
    elif plot_style == 'join centres' :
      axes.plot( self.x_points, self.y_points, **plotter_kwargs )
    elif plot_style == 'stepped line' :
      # x_bin_edges = np.array( [ (x_centre - x_errors[0]) for x_centre, x_errors in zip(self.x_points, self.x_error_pairs) ] + [ self.x_points[-1]+self.x_error_pairs[-1][1] ] )
      # axes.hist( self.x_points, bins=x_bin_edges, weights=self.y_points, histtype='step', **plotter_kwargs )
      x_bin_edges = np.array( sum([ [ x_centre - x_errors[0], x_centre + x_errors[1] ] for x_centre, x_errors in zip(self.x_points, self.x_error_pairs) ], [] ) )
      y_bin_edges = np.array( sum([ [ y_centre, y_centre ] for y_centre in self.y_points ], [] ) )
      axes.plot( x_bin_edges, y_bin_edges, drawstyle='steps', **plotter_kwargs )
    else :
      raise NotImplementedError( 'Style "{0}"" not recognised by {1}'.format( plot_style, type(self) ) )
