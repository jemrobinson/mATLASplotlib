import matplotlib.pyplot as pyplot
from matplotlib.patches import Polygon

class BaseCanvas(object) :
  '''Base class for canvas properties'''
  def __init__( self, n_pixels ) :
    self.figure = pyplot.figure( figsize=(n_pixels[0]/100.0, n_pixels[1]/100.0), dpi=100, facecolor='white' )
    # self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
    # self.log_type = '' if log_type == None else log_type
    # self.x_ticks = x_ticks
    # self.minor_x_ticks = [ 60, 200, 300, 500 ]
    # self.n_y_ticks = 4
    # self.main_legend = None
    # self.location_map = { 'upper right':['right','top'], 'upper left':['left','top'], 'lower right':['right','bottom'], 'lower left':['left','bottom'] }
    self.legend_order = []
    self.axis_ranges = {}
    self.plots = {}


  def add_plottable( self, plottable, axes='main', **kwargs ) :
    plottable.draw_on_plot( self.plots[axes], **kwargs )
    if 'label' in kwargs and kwargs['label'] != None and kwargs['label'] != '' and kwargs['label'] not in self.legend_order :
      self.legend_order.append( kwargs['label'] )


  def apply_plot_formatting( self ) :
    raise NotImplementedError( 'apply_plot_formatting not defined by {0}'.format(type(self)) )


  def draw_legend( self, x, y, axes, anchor_to='lower left', fontsize='small' ) :
    handles, labels = self.get_legend_handles_labels( self.plots[axes] )
    self.main_legend = self.plots[axes].legend( handles, labels, numpoints=1, loc=anchor_to, bbox_to_anchor=(x, y), bbox_transform=self.figure.transFigure )
    self.main_legend.get_frame().set_linewidth(0)
    self.main_legend.get_frame().set_alpha(0.0)
    pyplot.setp( self.main_legend.get_texts(), fontsize=fontsize )
    [ text.set_va('bottom') for text in self.main_legend.get_texts() ]


  def save_to_file( self, output_name ) :
    self.apply_plot_formatting()
    pyplot.savefig( '{0}.pdf'.format( output_name ) )
    print 'Saved figure to: {0}.pdf'.format( output_name )
    # self.close()


  def set_range( self, axis_name, axis_range ) :
    raise NotImplementedError( 'set_range not defined by {0}'.format(type(self)) )


  def get_legend_handles_labels( self, axes ) :
    # Remove duplicates
    handles, labels, seen = [], [], set()
    old_handles, old_labels = axes.get_legend_handles_labels()
    for handle, label in zip( old_handles, old_labels ) :
      if label not in seen :
        seen.add( label )
        labels.append( label )
        # if isinstance( handle, Polygon ) :
        #   proxy_artist = pyplot.Line2D( [0], [0], color=handle.properties()['edgecolor'], linestyle=handle.properties()['linestyle'] )
        #   handles.append( proxy_artist )
        # else :
        #   handles.append( handle )
        handles.append( handle )
    # Sort list of labels
    sorted_labels, sorted_handles = [], []
    for label in self.legend_order :
      idx_label = [ i for i,x in enumerate(labels) if x == label ]
      if len( idx_label ) > 0 :
        sorted_labels.append( labels.pop( idx_label[0] ) )
        sorted_handles.append( handles.pop( idx_label[0] ) )
    assert len(labels) == 0; assert len(handles) == 0
    return sorted_handles, sorted_labels
