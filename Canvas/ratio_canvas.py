from base_canvas import BaseCanvas
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, MaxNLocator
from numpy import arange

class RatioCanvas(BaseCanvas) :
  '''Simple canvas with standard ATLAS setup'''
  def __init__( self, n_pixels=(600,600) ) :
    super(RatioCanvas, self).__init__( n_pixels )
    self.plots['top'] = self.figure.add_axes( [0.15, 0.35, 0.8, 0.6] )
    self.plots['bottom'] = self.figure.add_axes( [0.15, 0.1, 0.8, 0.25] )


  def add_plottable( self, plottable, axes='top', **kwargs ) :
    super(RatioCanvas, self).add_plottable( plottable, axes, **kwargs )
    if 'x' not in self.axis_ranges : self.set_range( 'x', self.plots[axes].get_xlim() )
    if axes == 'top' :
      if 'y' not in self.axis_ranges : self.set_range( 'y', self.plots[axes].get_ylim() )
    elif axes == 'bottom' :
      if 'y_ratio' not in self.axis_ranges : self.set_range( 'y_ratio', self.plots[axes].get_ylim() )


  def set_range( self, axis_name, axis_range ) :
    if axis_name == 'x' :
      self.axis_ranges['x'] = axis_range
    elif axis_name == 'y' :
      self.axis_ranges['y'] = axis_range
    elif axis_name == 'y_ratio' :
      self.axis_ranges['y_ratio'] = axis_range
    else :
      raise ValueError( 'axis {0} not recognised by {1}'.format(axis_name,type(self)) )


  def apply_plot_formatting( self ) :
    if 'x' in self.axis_ranges :
      self.plots['top'].set_xlim( self.axis_ranges['x'] )
      self.plots['bottom'].set_xlim( self.axis_ranges['x'] )
    if 'y' in self.axis_ranges :
      self.plots['top'].set_ylim( self.axis_ranges['y'] )
    if 'y_ratio' in self.axis_ranges :
      self.plots['bottom'].set_ylim( self.axis_ranges['y_ratio'] )


    # Draw line at y = 1.0
    self.plots['bottom'].add_line( Line2D( self.axis_ranges['x'], [1, 1], transform=self.plots['bottom'].transData, linewidth=1, linestyle='--', color='black') )

    # Set ratio plot to linear scale
    self.plots['bottom'].set_yscale('linear')

    # Remove bottom-most tick from top-plot and top-and-bottom from bottom-plot
    self.plots['top'].yaxis.set_major_locator( MaxNLocator(nbins=len(self.plots['top'].get_yticklabels()), prune='lower') )
    self.plots['bottom'].yaxis.set_major_locator( FixedLocator( self.get_ratio_ticks( self.axis_ranges['y_ratio'] ) ) )

    # Remove tick-labels from top-plot
    self.plots['top'].set_xticklabels( [], minor=True )
    self.plots['top'].set_xticklabels( [], major=True )


  def draw_legend( self, x, y, axes='top', anchor_to='lower left' ) :
    super(RatioCanvas, self).draw_legend( x, y, axes=axes, anchor_to=anchor_to )

  def get_ratio_ticks( self, axis_range, n_approximate=4 ) :
    # Choose ratio ticks to be sensibly spaced and always include 1.0
    interval_estimate = abs(axis_range[1] - axis_range[0]) / float(n_approximate)
    tick_sizes = [ 0.001, 0.002, 0.005, 0.01, 0.02, 0.04, 0.05, 0.1, 0.2, 0.4, 0.5, 1.0, 2.0 ]
    # tick_idx = ( np.abs( np.array(tick_sizes)-interval_estimate ) ).argmin()
    # print interval_estimate, tick_idx, tick_sizes[tick_idx], 'vs.',
    tick_size = min( tick_sizes, key=lambda x:abs(x-interval_estimate) )
    return arange( 1.0-10*tick_size, 1.0+10*tick_size, tick_size )