import matplotlib.pyplot as pyplot
import matplotlib.ticker as tkr
from matplotlib.patches import Polygon

# Set fonts to Helvetica and stixsans (the only sans-serif maths font)
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Helvetica'
rcParams['mathtext.fontset'] = 'stixsans'

class BaseCanvas(object) :
  ## Class-level variables
  location_map = { 'upper right':['right','top'], 'upper left':['left','top'], 'lower right':['right','bottom'], 'lower left':['left','bottom'] }

  '''Base class for canvas properties'''
  def __init__( self, n_pixels, **kwargs ) :
    ## Set up figure
    self.figure = pyplot.figure( figsize=(n_pixels[0]/100.0, n_pixels[1]/100.0), dpi=100, facecolor='white' )

    ## Set properties from arguments
    self.log_type = kwargs.get( 'log_type', '' )
    self.x_ticks = kwargs.get( 'x_ticks', None )
    self.minor_x_ticks = kwargs.get( 'minor_x_ticks', [] )
    # self.n_y_ticks = 4
    # self.main_legend = None

    ## Set up value holders
    self.legend_order = []
    self.axis_ranges = {}
    self.plots = {}


  def add_plottable( self, plottable, axes, **kwargs ) :
#     if visible_label != None : text = text+'@'+visible_label
    legend_text = kwargs.pop('visible_label','')+'@'
    if legend_text is '@' : legend_text = kwargs.get('label','')
    if legend_text is not None and legend_text is not '' and legend_text not in self.legend_order :
      self.legend_order.append( legend_text )
    plottable.draw_on_plot( self.plots[axes], **kwargs )

#     # Fill list of labels - kept in same order as that in which plots were added
#     if plot != 'bottom' :
#       legend_text = text if visible_label == None else visible_label
#       if legend_text != None and legend_text != '' and legend_text not in self.legend_order :
#         self.legend_order.append( legend_text )


  def apply_plot_formatting( self ) :
    # Set useful axis properties
    for axes in self.figure.axes :
      # Draw x ticks
      if self.x_ticks is not None :
        x_interval = ( self.axis_ranges['x'][1] - self.axis_ranges['x'][0] ) / (len(self.x_ticks)-1)
        axes.xaxis.set_major_locator( tkr.MultipleLocator(x_interval) )
        axes.set_xticklabels( [''] + self.x_ticks ) # for some reason the first label is getting lost

      # Don't shift axis labels
      axes.yaxis.get_major_formatter().set_useOffset(False)

      # Draw minor ticks
      axes.xaxis.set_minor_locator( tkr.AutoMinorLocator() )
      axes.yaxis.set_minor_locator( tkr.AutoMinorLocator() )

      # Set x-axis log
      if 'x' in self.log_type :
        axes.set_xscale( 'log', subsx=[2, 3, 4, 5, 6, 7, 8, 9] )
        axes.xaxis.set_major_formatter( tkr.ScalarFormatter() )
        axes.xaxis.set_minor_formatter( tkr.FuncFormatter(self.minor_tick_format_function) ) # only show certain minor labels

      # Set y-axis log
      if 'y' in self.log_type :
        axes.set_yscale('log', subsy=[2, 3, 4, 5, 6, 7, 8, 9] )


  def draw_ATLAS_text( self, x, y, axes, anchor_to='lower left', plot_type=None ) :
    [ha, va], offset = self.location_map[anchor_to], 0.145
    if ha == 'right' : x, offset = x-0.225, 0.225 # shift leftwards if using a right-align
    self.plots[axes].text( x, y, 'ATLAS', style='italic', fontsize=17, fontweight='bold', ha=ha, va=va, transform=self.figure.transFigure )
    if plot_type is not None :
      self.plots[axes].text( x+offset, y, plot_type, fontsize=17, fontweight='bold', ha=ha, va=va, transform=self.figure.transFigure )


  def draw_legend( self, x, y, axes, anchor_to='lower left', fontsize=None, **kwargs ) :
    handles, labels = self.get_legend_handles_labels( self.plots[axes] )
    self.main_legend = self.plots[axes].legend( handles, labels, numpoints=1, loc=anchor_to, bbox_to_anchor=(x, y), bbox_transform=self.figure.transFigure, **kwargs )
    self.main_legend.get_frame().set_linewidth(0)
    self.main_legend.get_frame().set_alpha(0.0)
    if fontsize is not None : pyplot.setp( self.main_legend.get_texts(), fontsize=fontsize )
    [ text.set_va('bottom') for text in self.main_legend.get_texts() ]


  def draw_luminosity_text( self, x, y, luminosity_value, axes, anchor_to='lower left' ) :
    ha, va = self.location_map[anchor_to]
    self.plots[axes].text( x, y, r'$\mathrm{\mathsf{\sqrt{s}}} = 7\,\mathrm{\mathsf{TeV}} \, \int \mathcal{L} \mathrm{dt} = $'+luminosity_value, ha=ha, va=va, transform=self.figure.transFigure, fontsize=14 )


  def draw_text( self, x, y, extra_value, axes, anchor_to='lower left' ) :
    ha, va = self.location_map[anchor_to]
    self.plots[axes].text( x, y, extra_value, ha=ha, va=va, transform=self.figure.transFigure, fontsize=16 )


  def get_legend_handles_labels( self, axes ) :
    # Remove duplicates
    handles, labels, seen = [], [], set()
    old_handles, old_labels = axes.get_legend_handles_labels()
    for handle, label in zip( old_handles, old_labels ) :
      visible_label = label if label.find('@') == -1 else label.split('@')[1]
      if visible_label not in seen :
        seen.add( visible_label )
        labels.append( visible_label )
        if isinstance( handle, Polygon ) :
          proxy_artist = pyplot.Line2D( [0], [0], color=handle.properties()['edgecolor'], linestyle=handle.properties()['linestyle'] )
          handles.append( proxy_artist )
        else :
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


  def minor_tick_format_function( self, x, pos ) :
    if any( int(x) == elem for elem in self.minor_x_ticks ) :
      return '{0:.0f}'.format( x )
    return ''


  def save_to_file( self, output_name ) :
    self.apply_plot_formatting()
    pyplot.savefig( '{0}.pdf'.format( output_name ) )
    print 'Saved figure to: {0}.pdf'.format( output_name )
    pyplot.close( self.figure )


  def set_axis_label( self, axis_name, axis_label ) :
    raise NotImplementedError( 'set_label not defined by {0}'.format(type(self)) )


  def set_axis_range( self, axis_name, axis_range ) :
    raise NotImplementedError( 'set_axis_range not defined by {0}'.format(type(self)) )
