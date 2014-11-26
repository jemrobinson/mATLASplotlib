import matplotlib.pyplot as pyplot

class BaseCanvas(object) :
  '''Base class for canvas properties'''
  def __init__( self, n_pixels ) : #, log_type=None, x_ticks=None, ) :
    self.figure = pyplot.figure( figsize=(n_pixels[0]/100.0, n_pixels[1]/100.0), dpi=100, facecolor='white' )
    # self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
    # self.log_type = '' if log_type == None else log_type
    # self.x_ticks = x_ticks
    # self.minor_x_ticks = [ 60, 200, 300, 500 ]
    # self.n_y_ticks = 4
    # self.main_legend = None
    # self.location_map = { 'upper right':['right','top'], 'upper left':['left','top'], 'lower right':['right','bottom'], 'lower left':['left','bottom'] }
    # self.legend_order = []
    self.axis_ranges = {}
    self.plots = {}

  def add_plottable( self, plottable, plot='main', **kwargs ) : #format=None, style='errorbar', colour=None, label=None, visible_label=None, marker=None, markerfill=None, xerr=True, **kwargs ) :
    print 'Plotting a {0} in base.py'.format( type(plottable) )
    plottable.draw_on_plot( self.plots[plot], **kwargs )

  def save_to_file( self, output_name ) :
    self.apply_plot_formatting()
    pyplot.savefig( '{0}.pdf'.format( output_name ) )
    print 'Saved figure to: {0}.pdf'.format( output_name )
    # self.close()

  def set_range( self, axis_name, axis_range ) :
    raise NotImplementedError( 'set_range not defined by {0}'.format(type(self)) )

  def apply_plot_formatting( self ) :
    pass

