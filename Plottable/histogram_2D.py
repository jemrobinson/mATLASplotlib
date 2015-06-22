from base_plottable import BasePlottable
import numpy as np
from matplotlib import __version__ as mpl_version
import matplotlib.pyplot as pyplot

class Histogram2D(BasePlottable) :
  '''Plottable 2-dimensional histogram, binned along the x and y axes'''
  def __init__( self, *args, **kwargs ) :
    super(Histogram2D, self).__init__( *args, **kwargs )


  # Constructor
  def construct_from_xedges_yedges_zvalues( self, x_bin_edges=None, y_bin_edges=None, z_values=None, z_errors=None ) :
    if x_bin_edges is None or y_bin_edges is None :
      self.x_bin_edges = np.array([])
      self.y_bin_edges = np.array([])
      self.z_values = np.array([])
      self.z_errors = np.array([])
    else :
      self.x_bin_edges = x_bin_edges
      self.y_bin_edges = y_bin_edges
      self.z_values = z_values
      self.z_errors = z_errors

    self.x_bin_centres = [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( self.x_bin_edges[:-1], self.x_bin_edges[1:] ) ]
    self.y_bin_centres = [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( self.y_bin_edges[:-1], self.y_bin_edges[1:] ) ]
    x_full, y_full = np.meshgrid( self.x_bin_centres, self.y_bin_centres )
    self.x_values = x_full.ravel()
    self.y_values = y_full.ravel()
    assert len( z_values ) == len( z_errors ) == len( self.x_values ) == len( self.y_values )
    print 'values', self.x_values, self.y_values, self.z_values
    for x, y, z in zip( self.x_values, self.y_values, self.z_values ) :
      print z, 'x=', x, 'y=', y


  def construct_from_TH2( self, input_TH2 ) :
    input_TH2.Print('all')
    x_edges = [ input_TH2.GetXaxis().GetBinLowEdge(bin) for bin in range(1,input_TH2.GetNbinsX()+2) ]
    y_edges = [ input_TH2.GetYaxis().GetBinLowEdge(bin) for bin in range(1,input_TH2.GetNbinsY()+2) ]
    z_values = [ input_TH2.GetBinContent(xbin,ybin) for xbin in range(1,input_TH2.GetNbinsX()+1) for ybin in range(1,input_TH2.GetNbinsY()+1) ]
    z_errors = [ input_TH2.GetBinError(xbin,ybin) for xbin in range(1,input_TH2.GetNbinsX()+1) for ybin in range(1,input_TH2.GetNbinsY()+1) ]
    self.construct_from_xedges_yedges_zvalues( x_edges, y_edges, z_values, z_errors )


  # Plotting behaviour
  def draw_on_plot( self, axes, **kwargs ) :
    plot_style = kwargs.pop( 'style', None )
    # kwargs['label'] = kwargs.pop('label',None)
    # kwargs['color'] = kwargs.pop('colour_primary','black')
    # kwargs['linewidth'] = kwargs.pop('linewidth',2)
    # kwargs['linestyle'] = kwargs.pop('linestyle','solid')
    # # Remove unused parameters
    # kwargs.pop('colour_secondary',kwargs['color'])
    # kwargs.pop('hatch',None)
    # # Set custom dash styling
    # width = kwargs.get('linewidth',1)
    # if kwargs['linestyle'] is 'dashed'  : kwargs['dashes'] = ( 3*width,1*width )
    # if kwargs['linestyle'] is 'dotted'  : kwargs['dashes'] = ( 1*width,1*width )
    # if kwargs['linestyle'] is 'dashdot' : kwargs['dashes'] = ( 2*width,1*width,1*width,1*width )
    #
    if mpl_version > '1.4.0' :
      axes.hist2d( self.x_values, self.y_values, weights=self.z_values, bins=(self.x_bin_edges,self.y_bin_edges) ) #, range=None, weights=None, cmin=None, cmax=None **kwargs )
    else :
      pyplot.hist2d( self.x_values, self.y_values, weights=self.z_values, bins=(self.x_bin_edges,self.y_bin_edges) )


    # if plot_style.startswith('point') :
    #   kwargs['marker'] = kwargs.pop( 'marker', 'o' ) # Set marker to dot if not set
    #   if 'xerror' in plot_style : kwargs['xerr'] = np.transpose( self.x_error_pairs )
    #   if 'yerror' in plot_style : kwargs['yerr'] = np.transpose( self.y_error_pairs )
    #   # Get error cap sizes
    #   if mpl_version > '1.4.0' :
    #     with_error_bar_caps = kwargs.pop( 'with_error_bar_caps', False )
    #     kwargs['capthick'] = [0,kwargs.get('linewidth')][with_error_bar_caps]
    #     kwargs['capsize'] = [0,2*kwargs.get('linewidth')][with_error_bar_caps]
    #   # else :
    #   #   print 'Matplotlib version {0} is too old to allow error bar caps'.format( mpl_version )
    #   # Disable linestyle
    #   kwargs['linestyle'] = 'None'
    #   axes.errorbar( self.x_points, self.y_points, fmt='', **kwargs )
    # elif plot_style == 'join centres' :
    #   axes.plot( self.x_points, self.y_points, **kwargs )
    # elif plot_style == 'stepped line' :
    #   x_bin_edges = np.array( sum([ [ x_centre - x_errors[0], x_centre + x_errors[1] ] for x_centre, x_errors in zip(self.x_points, self.x_error_pairs) ], [] ) )
    #   y_bin_edges = np.array( sum([ [ y_centre, y_centre ] for y_centre in self.y_points ], [] ) )
    #   axes.plot( x_bin_edges, y_bin_edges, drawstyle='steps', **kwargs )
    # else :
    #   raise NotImplementedError( 'Style "{0}" not recognised by {1}'.format( plot_style, type(self) ) )
