from base_canvas import BaseCanvas

class SimpleCanvas(BaseCanvas) :
  '''Simple canvas with standard ATLAS setup'''
  def __init__( self, n_pixels=(600,600) ) :
    super(SimpleCanvas, self).__init__( n_pixels )
    self.plots['main'] = self.figure.add_axes( [0.15, 0.1, 0.8, 0.85] )

  def add_plottable( self, plottable, plot='main', **kwargs ) :
    super(SimpleCanvas, self).add_plottable( plottable, plot, **kwargs )

  def set_range( self, axis_name, axis_range ) :
    if axis_name == 'x' : self.axis_ranges['x'] = axis_range
    if axis_name == 'y' : self.axis_ranges['y'] = axis_range

  def apply_plot_formatting( self ) :
    if 'x' in self.axis_ranges :
      print 'x',self.axis_ranges['x']
      self.plots['main'].set_xlim( self.axis_ranges['x'] )
    if 'y' in self.axis_ranges :
      print 'y',self.axis_ranges['y']
      self.plots['main'].set_ylim( self.axis_ranges['y'] )
      # # Set x and y limits
      # if self.xmin != self.xmax :
      #   ax.set_xlim( [self.xmin, self.xmax] )
