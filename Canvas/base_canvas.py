import matplotlib; matplotlib.use('PDF')
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

    ## Set up value holders
    self.legend_order = []
    self.axis_ranges = {}
    self.plots = {}


  def add_plottable( self, plottable, axes, **kwargs ) :
    legend_text = kwargs.pop('visible_label','')+'@'
    if legend_text is '@' : legend_text = kwargs.get('label','')
    if 'stack' in kwargs.get('style','') : legend_text = 'stack:'+legend_text
    if legend_text is not None and legend_text is not '' and legend_text not in self.legend_order :
      self.legend_order.append( legend_text )
    plottable.draw_on_plot( self.plots[axes], **kwargs )


  def apply_plot_formatting( self ) :
    # Set useful axis properties
    for axes in self.figure.axes :
      # Draw x ticks
      if self.x_ticks is not None :
        x_interval = ( self.axis_ranges['x'][1] - self.axis_ranges['x'][0] ) / len(self.x_ticks)
        axes.xaxis.set_major_locator( tkr.MultipleLocator(x_interval) )
        axes.set_xticklabels( [''] + self.x_ticks ) # for some reason the first label is getting lost

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


  def draw_ATLAS_text( self, x, y, axes, anchor_to='lower left', plot_type=None, coordinates='figure' ) :
    [ha, va] = self.location_map[anchor_to] #, offset = self.location_map[anchor_to], 0.145
    transform = self.translate_coordinates(coordinates, axes)
    if plot_type is None :
      self.plots[axes].text( x, y, 'ATLAS', fontsize=17, fontweight='bold', ha=ha, va=va, transform=transform )
    else :
      # Plot invisible text to get bounding box
      invisible_text = self.plots[axes].text( x, y, 'ATLAS {0}'.format(plot_type), alpha=0, fontsize=17, fontweight='bold', ha=ha, va=va, transform=transform )
      bounding_box = invisible_text.get_window_extent(renderer=self.get_renderer()).transformed( transform.inverted() )
      x_left, x_right = bounding_box.min[0], bounding_box.max[0]
      # Use bounding box to plot visible text
      self.plots[axes].text( x_left, y, 'ATLAS', style='italic', fontsize=17, fontweight='bold', ha='left', va=va, transform=transform )
      self.plots[axes].text( x_right, y, plot_type, fontsize=17, fontweight='bold', ha='right', va=va, transform=transform )


  def draw_legend( self, x, y, axes, anchor_to='lower left', fontsize=None, coordinates='figure', **kwargs ) :
    transform = self.translate_coordinates(coordinates, axes)
    handles, labels = self.get_legend_handles_labels( self.plots[axes] )
    self.main_legend = self.plots[axes].legend( handles, labels, numpoints=1, loc=anchor_to, bbox_to_anchor=(x, y), bbox_transform=transform, borderpad=0, borderaxespad=0, columnspacing=0, **kwargs )
    self.main_legend.get_frame().set_linewidth(0)
    self.main_legend.get_frame().set_alpha(0.0)
    if fontsize is not None : pyplot.setp( self.main_legend.get_texts(), fontsize=fontsize )
    [ text.set_va('bottom') for text in self.main_legend.get_texts() ]


  def draw_luminosity_text( self, x, y, luminosity_value, axes, sqrts=7, anchor_to='lower left', coordinates='figure' ) :
    ha, va = self.location_map[anchor_to]
    transform = self.translate_coordinates(coordinates, axes)
    self.plots[axes].text( x, y, r'$\mathrm{\mathsf{\sqrt{s}}} = '+str(sqrts)+'\,\mathrm{\mathsf{TeV}} \, \int \mathcal{L} \mathrm{dt} = $'+luminosity_value, ha=ha, va=va, transform=transform, fontsize=14 )


  def draw_text( self, x, y, extra_value, axes, anchor_to='lower left', coordinates='figure' ) :
    ha, va = self.location_map[anchor_to]
    transform = self.translate_coordinates(coordinates, axes)
    self.plots[axes].text( x, y, extra_value, ha=ha, va=va, transform=transform, fontsize=16 )


  def get_axis_label( self, axis_name ) :
    raise NotImplementedError( 'get_label not defined by {0}'.format(type(self)) )


  def get_axis_range( self, axis_name ) :
    if axis_name in self.axis_ranges.keys() :
      return self.axis_ranges[axis_name]
    else :
      raise ValueError( 'axis {0} not recognised by {1}'.format(axis_name,type(self)) )


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
    # Pre-sort legend order for stacks, which need reversing
    stack_labels = list( reversed( [ label.replace('stack:','') for label in self.legend_order if 'stack:' in label ] ) )
    stack_indices = [ idx for idx, label in enumerate(self.legend_order) if 'stack:' in label ]
    for idx, label in zip(stack_indices,stack_labels) : self.legend_order[idx] = label
    # Sort list of labels
    sorted_labels, sorted_handles = [], []
    for label in self.legend_order :
      idx_label = [ i for i,x in enumerate(labels) if x == label ]
      if len( idx_label ) > 0 :
        sorted_labels.append( labels.pop( idx_label[0] ) )
        sorted_handles.append( handles.pop( idx_label[0] ) )
    # Append non-mATLASplotlib labels
    for label, handle in zip( labels, handles ) :
      sorted_labels.append( label )
      sorted_handles.append( handle )
    # assert len(labels) == 0; assert len(handles) == 0
    return sorted_handles, sorted_labels


  def get_renderer(self) :
    if hasattr(self.figure.canvas, 'get_renderer'):
      # Some backends, such as TkAgg, have the get_renderer method, which makes this easy.
      renderer = self.figure.canvas.get_renderer()
    else:
      # Other backends do not have the get_renderer method, so we have a work
      # around to find the renderer.  Print the figure to a temporary file
      # object, and then grab the renderer that was used.
      import io
      self.figure.canvas.print_pdf(io.BytesIO())
      renderer = self.figure._cachedRenderer
    return renderer


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


  def set_axis_log( self, log_type ) :
    self.log_type = log_type

  def set_title( self, title ) :
    raise NotImplementedError( 'set_title not defined by {0}'.format(type(self)) )


  def translate_coordinates( self, coordinates, axes ) :
    if coordinates == 'axes' : return self.plots[axes].transAxes
    return self.figure.transFigure
