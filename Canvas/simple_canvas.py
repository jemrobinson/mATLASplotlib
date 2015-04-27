from base_canvas import BaseCanvas

class SimpleCanvas(BaseCanvas) :
  '''Simple canvas with standard ATLAS setup'''
  def __init__( self, n_pixels=(600,600), **kwargs ) :
    super(SimpleCanvas, self).__init__( n_pixels, **kwargs )
    self.plots['main'] = self.figure.add_axes( [0.15, 0.1, 0.8, 0.85] )

  def add_plottable( self, plottable, axes='main', **kwargs ) :
    super(SimpleCanvas, self).add_plottable( plottable, axes, **kwargs )
    if 'x' not in self.axis_ranges : self.set_range( 'x', self.plots[axes].get_xlim() )
    if 'y' not in self.axis_ranges : self.set_range( 'y', self.plots[axes].get_ylim() )


  def draw_legend( self, x, y, axes='main', anchor_to='lower left' ) :
    super(SimpleCanvas, self).draw_legend( x, y, axes=axes, anchor_to=anchor_to )


  def set_label( self, axis_name, axis_label ) :
    if axis_name == 'x' :
      self.plots['main'].set_xlabel( axis_label, size=16, position=(1.0, 0.0), va='top', ha='right' )
    elif axis_name == 'y' :
      self.plots['main'].set_ylabel( axis_label, size=16 )
      # yposition = 0.8 if len(axis_label) < 70 else 0.6
      # self.plots['main'].yaxis.set_label_coords( -0.13, yposition )
      self.plots['main'].yaxis.set_label_coords( -0.13, [0.6,0.8][len(axis_label) < 70] )
    else :
      raise ValueError( 'axis {0} not recognised by {1}'.format(axis_name,type(self)) )


  def set_range( self, axis_name, axis_range ) :
    if axis_name == 'x' :
      self.axis_ranges['x'] = axis_range
    elif axis_name == 'y' :
      self.axis_ranges['y'] = axis_range
    else :
      raise ValueError( 'axis {0} not recognised by {1}'.format(axis_name,type(self)) )


  def apply_plot_formatting( self ) :
    super(SimpleCanvas, self).apply_plot_formatting()
    if 'x' in self.axis_ranges :
      self.plots['main'].set_xlim( self.axis_ranges['x'] )
    if 'y' in self.axis_ranges :
      self.plots['main'].set_ylim( self.axis_ranges['y'] )
