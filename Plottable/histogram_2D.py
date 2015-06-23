from base_plottable import BasePlottable
import numpy as np
from matplotlib import __version__ as mpl_version
import matplotlib.pyplot as pyplot

class Histogram2D(BasePlottable) :
  '''Plottable 2-dimensional histogram, binned along the x and y axes'''
  def __init__( self, *args, **kwargs ) :
    super(Histogram2D, self).__init__( *args, **kwargs )

  ## Main constructor
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
    self.x_bin_centres = self.edges_to_centres( self.x_bin_edges )
    self.y_bin_centres = self.edges_to_centres( self.y_bin_edges )
    x_full_centres, y_full_centres = np.meshgrid( self.x_bin_centres, self.y_bin_centres, indexing='xy' )
    self.x_values = x_full_centres.ravel()
    self.y_values = y_full_centres.ravel()
    assert len( z_values ) == len( self.x_values ) == len( self.y_values )
    if z_errors is not None : assert len( z_values ) == len( z_errors )

  ## Construct from ROOT.TH2
  def construct_from_TH2( self, input_TH2 ) :
    x_bin_edges = [ input_TH2.GetXaxis().GetBinLowEdge(bin) for bin in range(1,input_TH2.GetNbinsX()+2) ]
    y_bin_edges = [ input_TH2.GetYaxis().GetBinLowEdge(bin) for bin in range(1,input_TH2.GetNbinsY()+2) ]
    ix_array, iy_array = np.meshgrid( range(1,len(x_bin_edges)), range(1,len(y_bin_edges)), indexing='xy' )

    z_values, z_errors = [], []
    for ix, iy in zip( ix_array.ravel(), iy_array.ravel() ) :
      z_values.append( input_TH2.GetBinContent(ix,iy) )
      z_errors.append( input_TH2.GetBinError(ix,iy) )
    self.construct_from_xedges_yedges_zvalues( x_bin_edges, y_bin_edges, z_values, z_errors )


  ## Plotting behaviour
  def draw_on_plot( self, axes, **kwargs ) :
    plot_style = kwargs.pop( 'style', None )
    if 'colour_map' in kwargs :
      kwargs['cmap'] = getattr( pyplot.cm, kwargs.pop('colour_map') )
    boundaries = kwargs.pop('bar_ticks',None)

    if plot_style == 'colourbar' :
      data_array, xedges, yedges, image = axes.hist2d( self.x_values, self.y_values, weights=self.z_values, bins=(self.x_bin_edges,self.y_bin_edges), **kwargs )
      axes_image = axes.imshow( data_array, extent=(yedges[0], yedges[-1], xedges[0], xedges[-1]), aspect='auto', **kwargs )
      colourbar =  axes.get_figure().colorbar( axes_image, ax=axes, boundaries=boundaries )
    else :
      raise NotImplementedError( 'Style "{0}" not recognised by {1}'.format( plot_style, type(self) ) )
